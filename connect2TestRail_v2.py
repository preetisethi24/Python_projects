from testrail import *
import pprint as pp
import csv
import sys
import time

TESTRAIL_URL='https://evaautomation.testrail.net'
TESTRAIL_USER='preeti.sethi@bowerswilkins.com'
TESTRAIL_PASSWORD='T803/9iXI8QnSivuBtZw-MdIipJ47qloq73gHX.YN'

client = APIClient(TESTRAIL_URL)
client.user = TESTRAIL_USER
client.password = TESTRAIL_PASSWORD

def timeit(func):
    def timed(*args, **kwargs):
        #logger = logging.getLogger(getLogStr())
        #logger.info("in %s"%(func.__name__))
        ts = time.time()
        result = func(*args, **kwargs)
        te = time.time()
        print("%r time %3.2f sec"%(func.__name__, te-ts))
        return result

    return timed

@timeit
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
        noOftestCases = len(client.send_get('get_cases/{}&suite_id={}'.format(projectId,_id)))
        #nameOfTestcases=[]
        #for testCase in testCases:
            #nameOfTestcases.append(testCase['title'])
    except APIError as e:
        print("*********Found error************", e)
    #return nameOfTestcases
    return noOftestCases

@timeit
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


def getRunCases(projectId,planId):
    '''
    :param projectID:
    :param planID:
    :return:
    '''
    testRuns = client.send_get('get_plan/%s' % (planId))
    totalTestsRun=[]
    for i in range(len(testRuns['entries'])):
        passed = testRuns['entries'][i]['runs'][0]['passed_count']
        failed = testRuns['entries'][i]['runs'][0]['failed_count']
        blocked = testRuns['entries'][i]['runs'][0]['blocked_count']
        passedWithComments = testRuns['entries'][i]['runs'][0]['custom_status3_count']
        knownFailure = testRuns['entries'][i]['runs'][0]['custom_status1_count']
        notRun = testRuns['entries'][i]['runs'][0]['custom_status2_count']
        totalRun = passed+failed+blocked+passedWithComments+knownFailure+notRun
        totalTestsRun.append(totalRun)
    return(sum(totalTestsRun))

def getPercentage(totalCases,ranCases):
    """
    :param totalCases:
    :param ranCases:
    :return:
    """
    percentRan=(ranCases*100)/totalCases
    return percentRan

@timeit
def getTotalCases(projectId,planId):
    '''
    :param projectID:
    :param planID:
    :return:
    '''
    testRuns = client.send_get('get_plan/%s' % (planId))
    totalNumberOfTests=[]
    totalTestsRun = []
    for i in range(len(testRuns['entries'])):
        suiteId=testRuns['entries'][i]['runs'][0]['suite_id']
        suiteName=testRuns['entries'][i]['runs'][0]['name']
        noOfCases=getTestCase(projectId,suiteId)

        passed = testRuns['entries'][i]['runs'][0]['passed_count']
        failed = testRuns['entries'][i]['runs'][0]['failed_count']
        blocked = testRuns['entries'][i]['runs'][0]['blocked_count']
        passedWithComments = testRuns['entries'][i]['runs'][0]['custom_status3_count']
        knownFailure = testRuns['entries'][i]['runs'][0]['custom_status1_count']
        notRun = testRuns['entries'][i]['runs'][0]['custom_status2_count']
        totalRun = passed + failed + blocked + passedWithComments + knownFailure + notRun

        totalTestsRun.append(totalRun)
        totalNumberOfTests.append(noOfCases)

        print("Suitename: %s" %suiteName)
        print("Total no of cases for this Suite: %d" %noOfCases)
        print("Total no of cases per Suite ran on this tesplan: %d" %totalRun)
        print("Percentage run: %d" %getPercentage(noOfCases,totalRun))
        print("********************************")

    return sum(totalTestsRun),sum(totalNumberOfTests)


if (len(sys.argv)) < 3:
    print("Must give ProjectName and TestPlan name")
    print("Usage:connect2TestRail_v3.py projectname testplanname")
    sys.exit()

projectId = getProjectId(sys.argv[1])
planId = getTestPlanId(sys.argv[2])
totalTestsRun,totalNumberOfTests=getTotalCases(projectId,planId)

print("********************************************")
print("Total Cases: %d" %totalNumberOfTests)
print("Total Cases run: %d" %totalTestsRun)


