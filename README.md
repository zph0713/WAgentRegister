# WAgentRegister


*This tool was developed in Python 3*  


**Before Use**  
`pip3 install requirements.txt`
>certifi==2020.12.5
chardet==4.0.0  
idna==2.10  
numpy==1.20.3  
pandas==1.2.4  
prettytable==2.1.0  
python-dateutil==2.8.1  
pytz==2021.1  
requests==2.25.1  
six==1.16.0  
slack-sdk==3.5.1  
urllib3==1.26.4  
wcwidth==0.2.5  


**Settings**  
```cd conf/
vim settings.py
```



**Use guide**  
```cd bin/  
python3 var_manager.py --help
usage: war_manager.py [-h] [-r REMOVE_AGENTS_ARGS] [-R] [-m NOTIFICATION_MAIL] [-c CHECK_RESULTS_ARGS] [-C]
                      [-s SHOW_INFOMATION] [-a ADD_AGENTS_ARGS] [-A]

WAgentsRegister

optional arguments:
  -h, --help            show this help message and exit
  -r REMOVE_AGENTS_ARGS, --remove_agents_args REMOVE_AGENTS_ARGS
                        remove_agents
  -R, --remove_agents   remove_agents
  -m NOTIFICATION_MAIL, --notification_mail NOTIFICATION_MAIL
                        inotification_mail,example:{lost_agents|down_agents|to_add}
  -c CHECK_RESULTS_ARGS, --check_results_args CHECK_RESULTS_ARGS
                        install task results
  -C, --check_results   install task results
  -s SHOW_INFOMATION, --show_infomation SHOW_INFOMATION
                        show_infomation,example:{lost_agents|down_agents|to_add}
  -a ADD_AGENTS_ARGS, --add_agents_args ADD_AGENTS_ARGS
                        add_agents_args,install task results for arg,split used ','
  -A, --add_agents      add_agents,install task results,
```
