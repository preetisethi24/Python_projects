#!/usr/bin/python
#import requests
#sitedata=requests.get("https://evaautomation.testrail.net/index.php?/dashboard")

#with open("content.txt","w") as f:
#	f.write(sitedata.content)

from testrail import *
import pprint as pp
import csv
import sys

TESTRAIL_URL='https://evaautomation.testrail.net'
TESTRAIL_USER='preeti.sethi@bowerswilkins.com'
TESTRAIL_PASSWORD='T803/9iXI8QnSivuBtZw-MdIipJ47qloq73gHX.YN'

client = APIClient(TESTRAIL_URL)
client.user = TESTRAIL_USER
client.password = TESTRAIL_PASSWORD


def getProjectId(projectName):
    """
    returns projectId for projectName
    :param projectName:
    :return: projectId
    """
    try:
        projects = client.send_get('get_projects')
        for project in projects:
            if project['name'] == projectName:
                projectId=project['id']
    except APIError as e:
            print("*********Found error************", e)
    return projectId


def getSuiteId(projectId,suiteName):
    """
    returns suiteID for a given projectId and suiteName
    :param projectId:
    :param suiteName:
    :return: suiteId
    """
    try:
        testSuites = client.send_get('get_suites/%s'%(projectId))
        for testSuite in testSuites:
            if testSuite['name'] == suiteName:
                suiteId=testSuite['id']
    except APIError as e:
            print("*********Found error************", e)
    return suiteId

def getTestCase(projectId,suiteId):
    """
    returns a list of name of testcases
    :param projectId:
    :param suiteId:
    :return:nameOfTestcases
    """
    try:
        _id=suiteId
        testCases = client.send_get('get_cases/{}&suite_id={}'.format(projectId,_id))
        nameOfTestcases=[]
        for testCase in testCases:
            nameOfTestcases.append(testCase['title'])
    except APIError as e:
        print("*********Found error************", e)
    return nameOfTestcases


def getTestPlanId(testPlanName):
    """
    returns plainId for a giben testPlanName
    :param testPlanName:
    :return:planId
    """
    try:
        testPlans = client.send_get('get_plans/%s'%(projectId))
        for testPlan in testPlans:
            if testPlan['name'] == testPlanName:
                planId=testPlan['id']
    except APIError as e:
            print("*********Found error************", e)
    return planId


def getSuiteNames(planId):
    """
    returns name of the suites
    :param planId:
    :return:suiteNames
    """
    try:
        testRuns=client.send_get('get_plan/%s'%(planId))
        suiteNames=[]
        for i in range(len(testRuns['entries'])):
            suiteNames.append(testRuns['entries'][i]['name'])
    except APIError as e:
            print("*********Found error************", e)
    return suiteNames

#pp.pprint(client.send_get('get_plan/%s'%(687)))
#print("&&&&&&&&&&&&&&")
#pp.pprint(client.send_get('get_cases/1&suite_id=72'))



print("##########Calculating percentage of testing done#########")
projectId=getProjectId(sys.argv[1])
planId=getTestPlanId(sys.argv[2])
suiteNames=getSuiteNames(planId)
noOfTests=[]
for suiteName in suiteNames:
    #print("*******suite_name",suite_name)
    suiteId=getSuiteId(projectId,suiteName)
    #print("*******suite_id",suite_id)
    cases=getTestCase(projectId,suiteId)
    #print("*******cases",len(cases))
    noOfTests.append(len(getTestCase(projectId,suiteId)))
print("Total cases in the suite %d" %sum(noOfTests))
print("#################################")

with open (sys.argv[3]) as csvFile:
    csvReader = csv.reader(csvFile, delimiter=',')
    lineCount=0
    for row in csvReader:
        lineCount += 1
    print("Total no of cases ran %d" %lineCount)

percentRan=(lineCount*100)/sum(noOfTests)

print("#################################")
print("%d Percentage of testcases ran on this testcycle" %percentRan)
