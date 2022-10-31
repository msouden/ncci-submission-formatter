import csv23
from enum import Enum

#### Appends number to Account Number to make Line ID Number and iterates for each CPT

class CPTVal(Enum):
    CPTCode = 0
    CPTBilledCharges = 1
    CPTMod = 2
    CPTUnit = 3

####################### Define the Fixed Values for NCCI entries

CarrierCode = # 5 digit integer
TransactionCode = # 2 digit integer
ServiceFromDate = '00000000'
ServiceToDate = '00000000'
ProviderTaxonomyCode = # 10 digit string
ProviderIdNumber = # nine digit integer
NetworkServiceCode = # single char

########################################## filenames

reportFileName = 'NCCI QX YYYY DATA DD-MM-YYYY.csv'
claimantRosterFileName = # filename for roster.txt

######################################### Billing report strings (CSV)

ClaimString = 'Ins Claim Number'
BillDate = 'Date Bill Paid By Client'
ServiceDate = 'Date of Service'
CPT1 = 'CPT Code(s)'
Mod1 = 'Mod'
BilledCharges1 = 'Billed Charges'
RO1 = 'RO'
ProviderZip = 'Provider Zip'
Unit1 = 'Unit'
PlaceOfService = 'Place of Service'
FirstName = 'First Name',
LastName = 'Last Name'
CPT2 = 'CPT Code 2'
Mod2 = 'Mod 2'
BilledCharges2 = 'Billed Chgs 2'
RO2 = 'RO2'
Unit2 = 'Unit 2'
DOB = 'DOB'
CPT3 = 'CPT Code 3'
Mod3 = 'Mod 3'
BilledCharges3 = 'Billed Chgs 3'
Unit3 = 'Unit 3'
CPT4 = 'CPT Code 4'
Mod4 = 'Mod 4'
BilledCharges4 = 'Billed Chgs 4'
Unit4 = 'Unit 4'
CPT5 = 'CPT Code 5'
Mod5 = 'Mod 5'
BilledCharges5 = 'Billed Chgs 5'
Unit5 = 'Unit 5'
CPT6 = 'CPT Code 6'
Mod6 = 'Mod 6'
BilledCharges6 = 'Billed Chgs 6'
Unit6 = 'Unit 6'

######### Defines the column locations for items in claim roster 
######### via column offsets- location & lengths

RosterClaimOffset = 312
RosterClaimLength = 7
RosterPolicyIdentifierOffset = 355
RosterPolicyIdentifierLength = 8
RosterPolicyEffectiveDateOffset = 1206
RosterPolicyEffectiveDateLength = 10
RosterJurisdictionCodeOffset = 1394
RosterJurisdictionCodeLength = 2
RosterGenderCodeOffset = 141
RosterGenderCodeLength = 1
RosterBirthYearOffset = 137
RosterBirthYearLength = 4
RosterAccidentDateOffset = 334
RosterAccidentDateLength = 10
RosterLastNameOffset = 11
RosterLastNameLength = 35
# Any additional data needed from the roster is located by column and added here


########################### Billing Report Parsing ########################

# parses billing report into reportFileName
def parseBillingReport(reportFileName, errors):
    # claims the name of the dictionary indexed by the claim number
    claims = {}
    # columnNames is a list of all the columns, filled when we parse the first line
    columnNames = []

    errors.append('Errors Found while parsing billing report')
    errors.append('  Currently where no account number exists or Account Number = Account Number')
    with open(reportFileName) as csv_file:
        csv_reader = csv23.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            # first line we read we assume is the columns
            if line_count == 0:
                for i, rowTitle in enumerate(row):
                    columnNames.append(rowTitle.strip())
#                    if i == 0 and rowTitle.strip() != 'Ins Claim Number':
#                        throw
                line_count += 1
            # every line after that is data
            else:
                if columnNames:
                    # create a newDict for this row and fill it out
                    newDict = {}
                    for i, name in enumerate(columnNames):
                        newDict[name] = row[i].strip().upper()
                    # add this new dict to claims dict with key ClaimString
                    if newDict['Account Number'] and newDict['Account Number'] != 'Account Number':
                        claims[newDict[ClaimString]] = newDict
                    else:
                        error = ""
                        for data in row:
                            error += data + ','
                        error += '\n'
                        errors.append(error)
            
    return claims
######################## End Billing Report Parsing ####################################

####################### Begin Re-Formatting Roster Items ##############################

# Altering Date format 
# reverse case (TRUE) 10/12/2018 -> 20181012
# not reverse (FALSE) 2018/10/12 -> 20181012
def fixDate(dateString, reverse):
    if reverse:
        return dateString[6:10] + dateString[0:2] + dateString[3:5]
    else:
        return dateString[0:4] + dateString[5:7] + dateString[8:10]

# Turns Gender into Gender Code
def fixGender(genderString):
    if genderString == 'M':
        return '1'
    else:
        return '2'

# Enhance formatting on RO codes
def fixRO(roFormat):
    if len(roFormat) > 3:
        if '.' not in roFormat:
            roFormat = roFormat[:3] + '.' + roFormat[3:]
    else:
        roFormat = roFormat.replace('.','')
    return roFormat

#Strips formatting and decimal from money
def fixMoney(money):
    for char in ('$,." '):
        money = money.replace(char,'')
    return money.zfill(11)   


################# Roster File Parsing #######################

# Parses and formats data from the Roster text file 
def parseRoster(rosterFileName):
    claimantRoster = {}
#    errors = []         <------  ? why errors here and how to comapare betwixt dicts?
    with open(rosterFileName) as inputFile:
        lines = inputFile.readlines()
        for line in lines:
            newDict = {}
            lastName = line[RosterLastNameOffset:RosterLastNameOffset+RosterLastNameLength].strip()
            newDict['LastName'] = lastName

            claimNumber = line[RosterClaimOffset:RosterClaimOffset+RosterClaimLength]
            newDict['ClaimNumber'] = claimNumber
            
            policyID = line[RosterPolicyIdentifierOffset:RosterPolicyIdentifierOffset+RosterPolicyIdentifierLength]
            newDict['PolicyID'] = policyID

            effectiveDate = line[RosterPolicyEffectiveDateOffset:RosterPolicyEffectiveDateOffset+RosterPolicyEffectiveDateLength]
            newDict['EffectiveDate'] = fixDate(effectiveDate, True)
            
            jurisdictionCode = line[RosterJurisdictionCodeOffset:RosterJurisdictionCodeOffset+RosterJurisdictionCodeLength]
            newDict['Jurisdiction'] = jurisdictionCode

            genderCode = line[RosterGenderCodeOffset:RosterGenderCodeOffset+RosterGenderCodeLength]
            newDict['GenderCode'] = fixGender(genderCode)
            
            birthYear = line[RosterBirthYearOffset:RosterBirthYearOffset+RosterBirthYearLength]
            newDict['BirthYear'] = birthYear
            
            accidentDate = line[RosterAccidentDateOffset:RosterAccidentDateOffset+RosterAccidentDateLength]
            newDict['AccidentDate'] = fixDate(accidentDate, True)

            # Any additional data needed from the roster is defined here

            # if jurisdictionCode is None:    - will alter this to remove Location code 21 if needed
            #     jurisdictionCode = '  '

            # add the newDict to the roster dictionary
            claimantRoster[claimNumber] = newDict

    return claimantRoster

##### Cycles through CPT codes and adds enum values for CPT, Billed Charges, Mods, and Units 

def getCPTCodes(report):
    CPTData = []
    if report[CPT1] != '':
        data = []
        data.append(report[CPT1])
        data.append(report[BilledCharges1])
        data.append(report[Mod1])
        data.append(report[Unit1])
        CPTData.append(data)
    if report[CPT2] != '':
        data = []
        data.append(report[CPT2])
        data.append(report[BilledCharges2])
        data.append(report[Mod2])
        data.append(report[Unit2])
        CPTData.append(data)
    if report[CPT3] != '':
        data = []
        data.append(report[CPT3])
        data.append(report[BilledCharges3])
        data.append(report[Mod3])
        data.append(report[Unit3])
        CPTData.append(data)
    if report[CPT4] != '':
        data = []
        data.append(report[CPT4])
        data.append(report[BilledCharges4])
        data.append(report[Mod4])
        data.append(report[Unit4])
        CPTData.append(data)
    if report[CPT5] != '':
        data = []
        data.append(report[CPT5])
        data.append(report[BilledCharges5])
        data.append(report[Mod5])
        data.append(report[Unit5])
        CPTData.append(data)
    if report[CPT6] != '':
        data = []
        data.append(report[CPT6])
        data.append(report[BilledCharges6])
        data.append(report[Mod6])
        data.append(report[Unit6])
        CPTData.append(data)
    return CPTData

#################################### The reportMaker ###########################

def NCCIReportMaker(billingReport, claimantRoster,errors):
    # NCCI is an array of strings ending in newlines
    NCCI = []
    errors.append('\n\nErrors while generating output report')
    for claimNumber, report in billingReport.items():
        if claimNumber not in claimantRoster:
            error = ""
            errors.append('\nMissing claimNumber from roster:\n')
            for key in report:
                error += report[key] + ','
            error += '\n'
            errors.append(error)
        else:
            roster = claimantRoster[claimNumber]
            if report[LastName].upper() != roster['LastName'].upper():
                error = ""
                errors.append('\nLast Name mismatch:\n')
                for key in report:
                    error += report[key] + ','
                error += '\n'
                errors.append(error)
            #if billingReport.claimNumber.LastName != roster.claimNumber.LastName
            #   then add billingreport.claimNumber to errors.txt with "Last Name Mismatch" 
            CPTData = getCPTCodes(report)
            for i, cptdata in enumerate(CPTData):
                line = ''
                line = '{:23}'.format(CarrierCode + roster['PolicyID'])
                line += '{:20}'.format(roster['EffectiveDate'] + roster['ClaimNumber'])
                line += '{}'.format(TransactionCode + roster['Jurisdiction'] + roster['GenderCode'])
                line += '{}'.format(roster['BirthYear'] + roster['AccidentDate'])
                line += '{:38}'.format(fixDate(report[BillDate],False) + report['Account Number'])
                accountString = '{}0{}'.format(report['Account Number'], i + 1)
                line += '{:30}'.format(accountString)
                line += '{:49}'.format(fixDate(report[ServiceDate],False) + '0000000000000000' + cptdata[0])
                line += '{:8}'.format(cptdata[2])
                line += '{:36}'.format(fixMoney(cptdata[1]) + fixMoney(cptdata[1]) + fixRO(report[RO1]))
                line += '{:14}'.format(fixRO(report[RO2]))
                line += '{:20}'.format(ProviderTaxonomyCode)
                line += '{:15}'.format(ProviderIdNumber)
                line += '{}'.format(report['Provider Zip'][0:3] + NetworkServiceCode + cptdata[3].zfill(7) + report['Place of Service'])
                line += '\n'
                NCCI.append(line)
    return NCCI


###### Recording Errors Here ####
    # NCCI_errors = []
    # for claimNumber, report in billingReport.items():
    #     roster = claimantRoster[claimNumber]
    #     if roster == '':
    #         line += '{}'.format(roster['ClaimNumber']) + " was not found in Roster" 
    #         line += '\n'
    #         break
    #         NCCI_errors.append(line)
    # return NCCI_errors


def writeReportToFile(report, outputFileName):
    with open(outputFileName, 'w') as outputFile:
        for line in report:
            outputFile.write(line)

def main():
    errors = []

    billingReport = parseBillingReport(reportFileName, errors)

    claimantRoster = parseRoster(claimantRosterFileName)

    NCCIReport = NCCIReportMaker(billingReport, claimantRoster, errors)
    writeReportToFile(NCCIReport,'NCCI Q4 2018 DATA 2-5-19.2-output.txt')
    
    writeReportToFile(errors,'NCCI Q4 2018 DATA 2-5-19.2-NCCI_Report_errors.txt')


main()