from flask import Flask, request, jsonify, json
from flask_restful import reqparse, abort, Api, Resource
import os, requests
from datetime import datetime, date, timedelta

app = Flask(__name__)
api = Api(app)

# in-memory data for initial inventory and rental costs
inventory = { 
          "CHNS":{
          "tool_type": "chainsaw",
          "brand": "Stihl"},
          "LADW":{
          "tool_type": "ladder",
          "brand": "Werner"},
          "JAKD": {
          "tool_type": "jackhammer",
          "brand": "DeWitt"},
          "JAKR": {
          "tool_type": "jackhammer",
          "brand": "Ridgid"}
}

rental_cost = { 
          "ladder": {
          "daily": 1.99,
          "weekday": 'Yes',
          "weekend": 'Yes',
          "holiday": 'No'},
          "chainsaw": {
          "daily": 1.49,
          "weekday": 'Yes',
          "weekend": 'No',
          "holiday": 'Yes'},
          "jackhammer": {
          "daily": 2.99,
          "weekday": 'Yes',
          "weekend": 'No',
          "holiday": 'No'}
}

class Inventory(Resource):
    def get(self, tool_code=None):
        if not tool_code:
            return jsonify(data=inventory, status=200)
        if tool_code not in inventory:
            return abort(404, message="tool_code {} doesn't exist".format(tool_code))
        return jsonify(data={tool_code: inventory[tool_code]}, status=200)

    def put(self, tool_code=None):
        if not tool_code:
            return abort(400, message="tool_code is a required parameter")
        if tool_code not in inventory:
            return abort(404, message="tool_code {} doesn't exist".format(tool_code))
        inventory[tool_code] = {'tool_type': request.args.get('tool_type'), 'brand': request.args.get('brand')}
        return jsonify(data=inventory[tool_code], status=201)

    def post(self, tool_code=None):
        if not tool_code:
            return abort(400, message="tool code must be passed in the endpoint")
        data = request.args
        tool_type, brand = data["tool_type"], data["brand"]
        if not tool_type or not brand:
            return abort(400, message="missing necessary parameters {} for adding a tool".format(request.args.get('tool_code')))
        if tool_code in inventory:
            return abort(400, message="tool_code {} already exists in inventory".format(tool_code))
        inventory[tool_code] = {'tool_type': tool_type, 'brand': brand}
        return jsonify(data={tool_code: inventory[tool_code]}, status=201)

class RentalCost(Resource):
    def get(self, tool_type=None):
        if not tool_type:
            return abort(400, message="tool_type is required (ex. /api/v1.0/rental_cost/<tool_type>)")
        if tool_type not in rental_cost:
            return abort(404, message="tool_type {} is not in rental_cost".format(tool_type))
        return jsonify(data={tool_type: rental_cost[tool_type]}, status=200)

    def put(self, tool_type=None):
        if not tool_type:
            return abort(400, message="tool_type is required (ex. /api/v1.0/rental_cost/<tool_type>)")
        if tool_type not in rental_cost:
            return abort(404, message="tool_type {} not found in rental_cost".format(tool_type))
        '''
        checks to see what parameters were provided and update accordingly.
        the only required parameter is tool_type. so what is updated depends on what 
        parameters are provided. if for example someone only wants to 'weekday' from 
        'Yes' to 'No', PUT /api/v1.0/rental_cost/<tool_type>?weekday=No, 
        only that field will be updated
        '''
        daily = request.args.get("daily")
        weekday = request.args.get("weekday")
        weekend = request.args.get("weekend")
        holiday = request.args.get("holiday")
        if not daily:
            daily = rental_cost[tool_type]['daily']
        if not weekday:
            weekday = rental_cost[tool_type]['weekday']
        if not weekend:
            weekend = rental_cost[tool_type]['weekend']
        if not holiday:
            holiday = rental_cost[tool_type]['holiday']
        rental_cost[tool_type] = {'daily': daily, 'weekday': weekday, 'weekend': weekend, 'holiday': holiday}
        return jsonify(data={tool_type: rental_cost[tool_type]}, status=201)

    def post(self, tool_type=None):
        missing=[]
        if not tool_type:
            return abort(400, message="tool_type is required (ex. /api/v1.0/rental_cost/<tool_type>)")
        daily = request.args.get("daily")
        if not daily:
            missing.append(daily)            
        if not isinstance(daily, float):
            return abort(400, message="daily rate must be entered as a float data type (ex. 3.99)")
        weekday = request.args.get("weekday")
        if not weekday:
            missing.append("weekday")
        weekend = request.args.get("weekend")
        if not weekend:
            missing.append("weekend")
        holiday = request.args.get("holiday")
        if not holiday:
            missing.append("holiday")
        if missing:
            return abort(400, message="when adding a rental cost all parameters are required, the following were missing: "+' '.join(missing))
        rental_cost[tool_type] = {"daily": daily, "weekday": weekday, "weekend": weekend, "holiday": holiday}
        return jsonify(data={tool_type: rental_cost[tool_type]}, status=200)

class RentalAgreement(Resource):
    def checkLaborDay(self, s_yy, e_yy):
        '''
        returns the date of labor day for each year in rental period
        makes assumption all date ranges will be in the 20th century (i.e. 20xx)
        '''
        labor_days = set()
        for yy in range(e_yy, s_yy-1, -1):
            check_labor_day = 1
            day_of_week = None
            while day_of_week != 'Mon':
                check_labor_day += 1
                d = datetime(yy, 9, check_labor_day)
                day_of_week = d.strftime('%a')
            labor_days.add(str(date(int('20'+str(yy)), int('09'), int('0'+str(check_labor_day)))))
        return labor_days

    def rentalPeriod(self, checkout_date, rental_days):
        '''
        determines the date the tool is due back. 
        first checks if month is February, and if so, if it is a leap year.
        it then checks if it is a month with 31 days
        makes assumption all date ranges will be in the 20th century (i.e. 20xx)
        '''
        if not isinstance(rental_days, int):
            rental_days=int(rental_days)
            
        thirty_one_day_mths = [1,3,5,7,8,10,12]
        mm, dd, yy = [int(_) for _ in checkout_date.split('/')]

        while True:
            if mm > 12:
                mm = 1
                yy += 1
            if mm == 2:
                leap_day = 0
                if int('20'+str(yy))%400==0:
                    leap_day=1
                elif int('20'+str(yy))%100==0:
                    leap_day=0
                elif int('20'+str(yy))%4==0:
                    leap_day=1
                days = 28+leap_day
            elif mm in thirty_one_day_mths:
                 days=31
            else:
                days=30

            rental_days -= days
            rental_days += dd
            dd = 0

            if rental_days <= 0:
                break
            mm+= 1

        mm, dd, yy = str(mm), str(days+rental_days), str(yy)
        if len(mm) == 1:
            mm = '0'+mm

        if len(dd) == 1:
            dd = '0'+dd

        due_date = '/'.join([str(mm), dd, str(yy)])

        return due_date

    def getRentalCost(self, checkout_date, due_date, daily_rate, weekday, weekend, holiday, discount_percent):
        total_amt_due = 0
        if not isinstance(daily_rate, float):
            daily_rate = float(daily_rate)

        s_mm, s_dd, s_yy = checkout_date.split('/')
        e_mm, e_dd, e_yy = due_date.split('/')

        start_date, end_date = date(int('20'+s_yy), int(s_mm), int(s_dd)), date(int('20'+e_yy), int(e_mm), int(e_dd))

        # currently there are only 2 holidays. here we can add more holidays in the future.
        # if charges aren't applied for holidays or there are no holidays observed this will return an empty list
        holiday_lst = set()
        for _ in range(int(e_yy), int(s_yy)-1, -1):
            holiday_lst.add(str(date(int('20'+str(_)), int('07'), int('04'))))
            holiday_lst |= self.checkLaborDay(int(s_yy), int(e_yy))

        # determine the sum of daily rate for holiday, weekends and weekdays
        weekday_days, weekend_days, holiday_days = 0, 0, 0
        # this checks to determine if holidays are being observed, if this is empty it checks if date is a weekend or weekday
        for _ in range((end_date - start_date).days):
            if str(start_date + timedelta(_ + 1)) in holiday_lst:
                if holiday == 'Yes':
                    total_amt_due += daily_rate
                    holiday_days += 1
            elif (start_date + timedelta(_ + 1)).strftime('%a') in ['Sat', 'Sun']:
                weekend_days += 1
            else:
                weekday_days += 1

        # determine based on parameters if sum of daily rates should be applied to weekdays, weekends, and holidays
        if weekend == 'Yes':
            total_amt_due += (daily_rate*weekend_days)
        else:
            weekend_days = 0
        if weekday == 'Yes':
            total_amt_due += (daily_rate*weekday_days)
        else:
            weekday_days = 0

        total_amt_due = float(total_amt_due)
        discount_percent = round(float(discount_percent))

        discount_amt = 0.00
        discount_amt = total_amt_due*(discount_percent/100)

        discount_percent = str(int(discount_percent))+'%'
        final_amt_due = f'${total_amt_due-discount_amt:,.2f}'
        total_amt_due = f'${float(total_amt_due):,.2f}'
        discount_amt = f'${discount_amt:,.2f}'

        return total_amt_due, final_amt_due, discount_amt, weekday_days+weekend_days+holiday_days, discount_percent

    def get(self):
        missing = []
        tool_code = request.args.get("tool_code")
        if tool_code not in inventory:
            return abort(404, message="tool_code {} is not in inventory".format(tool_code))
        if not tool_code:
            missing.append('tool_code')
        rental_days = request.args.get("rental_days")
        if not rental_days:
            missing.append('rental_days')
        checkout_date = request.args.get("checkout_date")
        if not checkout_date:
            missing.append('checkout_date')
        discount_percent = request.args.get("discount_percent")
        if not discount_percent:
            missing.append('discount_percent')
        if missing:
            return abort(400, message="the following required parameters are missing "+''.join(missing))

        # return error if discount is greater than 100 percent or rental days is not 1 or greater
        if int(discount_percent) > 100:
            return abort(400, message="discount cannot be greater than 100 percent")
        if int(rental_days) < 1:
            return abort(400, message="there must be at least one rental day")
        
        tool_type = inventory[tool_code]['tool_type']
        brand = inventory[tool_code]['brand']

        if tool_type not in rental_cost:
            return abort(404, message="tool_type {} does not exist in rental_cost".format(tool_type))

        daily_rate, weekday_rate, weekend_rate, holiday_rate = [v for k,v in rental_cost[tool_type].items()]

        due_date = self.rentalPeriod(checkout_date, rental_days)
        total_cost, final_amt, discount_amt, charge_days, discount_percent = self.getRentalCost(checkout_date, due_date, daily_rate, weekday_rate, weekend_rate, holiday_rate, discount_percent)

        return jsonify({'Tool Code': tool_code, 'Tool Type': tool_type, 'Tool Brand': brand, 'Rental Days': rental_days, 'Check Out Date': checkout_date, 'Due Date': due_date, 'Daily Rental Charge': daily_rate, 'Charge Days': charge_days, 'Pre-Discount Charge': total_cost, 'Discount Percent': discount_percent, 'Discount Amount': discount_amt, 'Final Charge': final_amt})


api.add_resource(Inventory, '/api/v1.0/inventory', '/api/v1.0/inventory/<tool_code>')
api.add_resource(RentalCost, '/api/v1.0/rental_cost', '/api/v1.0/rental_cost/<tool_type>')
api.add_resource(RentalAgreement, '/api/v1.0/rental_agreement')

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
