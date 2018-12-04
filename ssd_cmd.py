# __author__ = 'admin'
import paramiko
class SSD(object):
    def Cmd(self,ip,user,password,port,cmd):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=ip, port=port, username=user, password=password)
        # cmd='cd /sys/block/dfa/shannon/;cat access_mode'
        stdin, stdout, stderr = ssh.exec_command(cmd)
        result = stdout.read()
        if not result:
            result = stderr.read()
        ssh.close()
        result_decode=result.decode()


        return  result_decode

    def excute_cmd(self,ip,user,password,port,cmd,to_ip,to_user,to_password,to_port):

        cmd1='cd /sys/block/dfa/shannon/;cat access_mode;cd /sys/block/dfa/shannon/;cat temperature_int;' \
         'cat temperature_flash;cat dynamic_bad_blkcnt;cat estimated_life_left;cat host_read_bandwidth;cat host_read_iops;' \
        'cat host_read_latency;cat host_write_bandwidth;cat host_write_iops;cat host_write_latency'
        cmd2='shannon-status -p /dev/scta|grep media_status;shannon-status -p /dev/scta|grep seu_flag'
        result1=SSD().Cmd(to_ip,to_user,to_password,to_port,cmd1)
        result2=SSD().Cmd(to_ip,to_user,to_password,to_port,cmd2)

        each_number= result1.splitlines()

        each_line=result2.splitlines()

        monitor_item_value={}
        monitor_item_value['Access Mode']=each_number[0][-9:]
        monitor_item_value['Controller Temperature']=each_number[1]
        monitor_item_value['Flash Temperature']=each_number[2]
        monitor_item_value['Dynamic Bad Blocks']=each_number[3]
        monitor_item_value['Estimated_Life_Left']=each_number[4]+'%'
        monitor_item_value['host_read_bandwidth']=each_number[5]
        monitor_item_value['host_read_iops']=each_number[6]
        monitor_item_value['host_read_latency']=each_number[7]
        monitor_item_value['host_write_bandwidth']=each_number[8]
        monitor_item_value['host_write_iops']=each_number[9]
        monitor_item_value['host_write_latency']=each_number[10]
        monitor_item_value['Media Status']=each_line[0][-7:]
        monitor_item_value['SEU Flag']=each_line[1][-6:]

        return monitor_item_value

