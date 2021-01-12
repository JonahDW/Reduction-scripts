import glob
import subprocess

gaintables = glob.glob('GAINTABLES/*')

for table in gaintables:
    gaintype = table.split('.')[-1][0].upper()
    output = 'GAINPLOTS/'+table.split('/')[-1]

    syscall = 'ragavi-gains -g '+gaintype+' -t '+table+' --htmlname='+output
    subprocess.run([syscall],shell=True)