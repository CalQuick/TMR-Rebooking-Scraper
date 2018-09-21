import os, sys, pprint, re, datetime

months = ('Jan', 'Feb', 'March', 'April', 'May', 'June', 'July', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec')

thisfile = os.path.basename(sys.argv[0])
#2371218 07/20/2018 07/21/2018 - is an example of the information to search for
datesRegex = re.compile(r'(\d{7}) (\d\d/\d\d/\d\d\d\d) (\d\d/\d\d/\d\d\d\d) .* (\d{2,4}\.\d\d)')


commissionRequired = ''    
while True:
    try:
        print('Please input commission rebooking threshold (0 will return all):')
        print('This is the value for how much commission you must receive to make the rebooking.')
        commissionRequired = float(input()) # How much commission you must earn to be worth phoning.
        if commissionRequired >= 0 :
            break
        else:
            print('Must enter a positive number')
    except ValueError:
        print('An error occured: You must enter a positive integer with no spaces')


resList = {}
orderedList = []

for file in os.listdir():
    number = 1
    if os.path.isfile(file) and file != thisfile and not (file).endswith(' - output.txt'):
        file = open(file)
        contents = file.read()
        mo = datesRegex.findall(contents) # Returns list of ('Reg#','Arrival date', 'Departure 
        
        for res in mo:

            depart = res[2].split('/')
            depart = datetime.date(int(depart[2]),int(depart[0]),int(depart[1]))

            arrive = res[1].split('/')
            month = int(arrive[0])
            arrive = datetime.date(int(arrive[2]),int(arrive[0]),int(arrive[1]))

            days = (depart - arrive).days
            rate = float(res[3])
            totalPrice = round(days * rate, 2)
            commission = round((0.008 * totalPrice), 2)

            resList[res[0]]={'days': days, 'rate': rate, 'totalPrice': totalPrice, 'tmr': 9*commission, 'commission': commission, 'month': month}
            orderedList.append([totalPrice, res[0]])
            
            if commission >= commissionRequired:
                print(str(number) + ') #' + res[0] + ' is staying in ' + months[month-1] + ' for ' + str(days) + ' days at $' + res[3] + ' per night. You would earn $' + str(commission) + ' in commission by reducing their rate by 10%.')
                print('TMR would make an additional $' + str(round(9*commission,2)) + ' by rebooking directly.')
                print()
                number += 1

        file.close()           

        orderedList.sort(reverse=True)
        output = open(file.name + ' - output.txt', 'w')
        output.write('----- List of reservations which can be rebooked directly. Ordered by most amount of money to be saved. -----\n\n\n')
        
        for num in range(len(orderedList)):
            resNum = orderedList[num][1]
            output.write(str(num+1) + ') Res #' + resNum + ' - ' + str(resList[resNum]['days']) + ' days at $' + str(resList[resNum]['rate']) + ' per day. Book direct at only $' + str(round(resList[resNum]['rate']*0.9,2)) + ' per day and TMR make an extra $' + str(round(resList[resNum]['tmr'],2)) + '. Commission = $' + str(resList[resNum]['commission']) + '\n\n')

        output.close()

        
pausescript = input('Press any key to close')
