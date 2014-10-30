def run_job(job, script=None):
    """
        Submits scripts as an R-job to cluster with qsub (SGE);
        This submission implements SCRIPTS concept in BREEZE
        (For REPOTS submission see run_report)
    """
    loc = str(settings.MEDIA_ROOT) + str(get_folder_name('jobs', job.jname, job.juser.username))
    config = loc + slugify(job.jname + '_' + job.juser.username) + '_config.sh'

    default_dir = os.getcwd()
    os.chdir(loc)

    job.status = "active"
    job.progress = 15
    job.save()

    s = drmaa.Session()
    s.initialize()

    jt = s.createJobTemplate()

    jt.workingDirectory = loc
    jt.jobName = slugify(job.jname) + '_JOB'
    jt.email = [str(job.juser.email)]
    jt.blockEmail = False
    jt.remoteCommand = config
    jt.joinFiles = True

    job.sgeid = s.runJob(jt)
    job.progress = 30
    job.save()

    SGEID = copy.deepcopy(job.sgeid)
    # waiting for the job to end
    retval = s.wait(SGEID, drmaa.Session.TIMEOUT_WAIT_FOREVER)
    job.progress = 100
    job.save()

    if retval.hasExited and retval.exitStatus == 0:
        job.status = 'succeed'

        # clean up the folder

    else:
        job.status = 'failed'

    job.save()

    os.chdir(default_dir)
    return True

def run_report(report):
    """
        Submits reports as an R-job to cluster with SGE;
        This submission implements REPORTS concept in BREEZE
        (For SCRIPTS submission see run_job)
    """
    loc = str(settings.MEDIA_ROOT) + report.home
    config = loc + '/sgeconfig.sh'

    default_dir = os.getcwd()
    os.chdir(loc)

    report.status = "active"
    report.progress = 15
    report.save()

    s = drmaa.Session()
    s.initialize()

    jt = s.createJobTemplate()

    jt.workingDirectory = loc
    jt.jobName = slugify(report.name) + '_REPORT'
    jt.email = [str(report.author.email)]
    jt.blockEmail = False
    jt.remoteCommand = config
    jt.joinFiles = True

    report.sgeid = s.runJob(jt)
    report.progress = 30
    report.save()

    # waiting for the job to end
    retval = s.wait(report.sgeid, drmaa.Session.TIMEOUT_WAIT_FOREVER)
    report.progress = 100
    report.save()

    if retval.hasExited and retval.exitStatus == 0:
        report.status = 'succeed'

        # clean up the folder

    else:
        report.status = 'failed'

    report.save()

    # aux.open_folder_permissions(loc, 0777)

    os.chdir(default_dir)
    return True
