#platforn=x86, AMD64, or Intel EM64T                                                                                                                                                                       
# System authorization information                                                                                                                                                                         
auth  --useshadow  --enablemd5                                                                                                                                                                             
# System bootloader configuration                                                                                                                                                                          
bootloader --location=mbr                                                                                                                                                                                  
# Partition clearing information                                                                                                                                                                           
clearpart --all --initlabel --drives=sda                                                                                                                                                                   
# Use text mode install                                                                                                                                                                                    
text                                                                                                                                                                                                       
# Firewall configuration                                                                                                                                                                                   
firewall --enabled                                                                                                                                                                                         
# Run the Setup Agent on first boot                                                                                                                                                                        
firstboot --disable                                                                                                                                                                                        
# System keyboard                                                                                                                                                                                          
keyboard us                                                                                                                                                                                                
# System language                                                                                                                                                                                          
lang en_US                                                                                                                                                                                                 
# Use network installation                                                                                                                                                                                 
url --url=http://10.204.217.158/contrail/images/centos-7.7                                                                                                                                                                                            
# If any cobbler repo definitions were referenced in the kickstart profile, include them here.                                                                                                             
repo --name=contrail-redhat-repo --baseurl=http://10.204.217.158/cobbler/repo_mirror/contrail-redhat-repo
                                                                                                                                                                                           
# Network information                                                                                                                                                                                      
# Reboot after installation                                                                                                                                                                                
reboot                                                                                                                                                                                                     

# Root password
rootpw --iscrypted $1$Ro1RlnFP$mYFiOzFoWoXbKgZTrA1DN1
# SELinux configuration   
selinux --disabled        
# Do not configure the X Window System
skipx                                 
# System timezone                     
#timezone  America/Los_Angeles         
timezone Asia/Kolkata
# Install OS instead of upgrade       
install                               
# Clear the Master Boot Record        
zerombr                               
# Allow anaconda to partition the system as needed
part /boot --fstype ext4 --size=1024
part swap --recommended
part pv.01      --size=1000     --grow  --ondisk=sda
volgroup nodeg20-vg00 pv.01
logvol /     --vgname=nodeg20-vg00 --fstype=ext4 --percent=85 --name=lv_root
logvol /tmp  --vgname=nodeg20-vg00 --fstype=ext4 --percent=10 --name=lv_tmp
logvol /home --vgname=nodeg20-vg00 --fstype=ext4 --percent=5  --name=lv_home
#logvol /var  --vgname=nodeg20-vg00 --fstype=ext4 --percent=30 --name=lv_var

%pre
set -x -v
exec 1>/tmp/ks-pre.log 2>&1

# Once root's homedir is there, copy over the log.
while : ; do
    sleep 10
    if [ -d /mnt/sysimage/root ]; then
        cp /tmp/ks-pre.log /mnt/sysimage/root/
        logger "Copied %pre section log to system"
        break
    fi
done &


wget "http://10.204.217.158/cblr/svc/op/trig/mode/pre/system/nodeg20" -O /dev/null
# Enable installation monitoring         
%end                                     

#repo --name=updates --baseurl="http://10.84.5.81/pulp/repos/centos74-updates/"
%packages --nobase
@core
openssh-clients
net-tools
#kernel-3.10.0-693.21.1.el7.x86_64



%end                                    

%post
set -x -v
exec 1>/root/ks-post.log 2>&1

yum install -y wget ntp ntpdate
yum -y install wget ntp ntpdate python-netaddr.noarch
wget -O /root/interface_setup.py http://10.204.217.158/kickstarts/interface_setup.py
wget -O /root/staticroute_setup.py http://10.204.217.158/kickstarts/staticroute_setup.py
wget -O /root/nodeg20.sh http://10.204.217.158/contrail/config_file/nodeg20.sh
chmod +x /root/nodeg20.sh
sed -i '1 a # chkconfig: 2345 80 20' /root/nodeg20.sh
sed -i '2 a # description: Interface and static route configuration entries' /root/nodeg20.sh
sed -i 's/Defaults    requiretty/#Defaults requiretty/g' /etc/sudoers
cp /root/nodeg20.sh /etc/init.d
cd /etc/init.d
/sbin/chkconfig --add nodeg20.sh
/sbin/chkconfig nodeg20.sh on
rm /root/nodeg20.sh

#Installing DG
wget -O /etc/yum.repos.d/JNPRR.repo http://10.204.226.33/REPO/Centos-7/JNPR.repo
wget -O /etc/yum.repos.d/main.repo http://10.204.226.33/REPO/Centos-7/main.repo
yum -y update
yum -y install datagather lynis jnprcfg-lynis
echo "nohup /opt/datagather/datagather-cron . &" >> /etc/rc.local
chmod +x /etc/rc.d/rc.local

/usr/sbin/ntpdate 10.204.217.158                                
/sbin/hwclock --systohc                                       
/bin/mv /etc/ntp.conf /etc/ntp.conf.orig                      
/bin/touch /var/lib/ntp/drift                                 
cat << __EOT__ > /etc/ntp.conf                                
driftfile /var/lib/ntp/drift
server 10.204.217.158  iburst
restrict 127.0.0.1
restrict -6 ::1
includefile /etc/ntp/crypto/pw
keys /etc/ntp/keys
__EOT__
/sbin/chkconfig ntpd on
/sbin/chkconfig
/sbin/service ntpd start

# Start yum configuration
wget "http://10.204.217.158/cblr/svc/op/yum/system/nodeg20" --output-document=/etc/yum.repos.d/cobbler-config.repo

# End yum configuration






echo "10.204.217.158 puppet" >> /etc/hosts
echo "10.204.217.60 nodeg20.englab.juniper.net nodeg20" >> /etc/hosts
echo "nodeg20" > /etc/hostname

# disable selinux and iptables
sed -i 's/SELINUX=.*/SELINUX=permissive/g' /etc/selinux/config
service iptables stop
/sbin/chkconfig iptables off

# Start download cobbler managed config files (if applicable)
# End download cobbler managed config files (if applicable)

# Start koan environment setup
echo "export COBBLER_SERVER=10.204.217.158" > /etc/profile.d/cobbler.sh
echo "setenv COBBLER_SERVER 10.204.217.158" > /etc/profile.d/cobbler.csh
# End koan environment setup

# begin Red Hat management server registration
# not configured to register to any Red Hat management server (ok)
# end Red Hat management server registration

# Begin cobbler registration
# skipping for system-based installation
# End cobbler registration

# Enable post-install boot notification
# Start final steps

wget "http://10.204.217.158/cblr/svc/op/ks/system/nodeg20" -O /root/cobbler.ks
wget "http://10.204.217.158/cblr/svc/op/trig/mode/post/system/nodeg20" -O /dev/null
wget "http://10.204.217.158/cblr/svc/op/nopxe/system/nodeg20" -O /dev/null
# End final steps
%end

