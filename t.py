import numpy as np
sub_pulse_times='[280e-6,1300e-6,690e-6,830e-6]'

#sub_pulse_times=np.format_float_scientific(np.float32(sub_pulse_times))
#sub_pulse_times= = np.float32(sub_pulse_times)
#sub_pulse_times=np.format_float_scientific(sub_pulse_times, unique=False, precision=15)
#sub_pulse_times=np.format_float_scientific(sub_pulse_times, exp_digits=4)
sub_pulse_times = np.fromstring(sub_pulse_times[1:-1],sep=',')
#sub_pulse_times=np.format_float_scientific(np.float32(sub_pulse_times))
t_start_lin = []
t_stop_lin = []
print(2*np.arange(len(sub_pulse_times)/2).astype(int))
t_start_lin = sub_pulse_times[2*np.arange(len(sub_pulse_times)/2).astype(int)]
t_stop_lin = sub_pulse_times[1+2*np.arange(len(sub_pulse_times)/2).astype(int)]
# for i in range(len(sub_pulse_times)):
#     if i%2:        
#         t_stop_lin.append(sub_pulse_times[i], axis=0)
#     else:
#         t_start_lin.append(sub_pulse_times[i])
print("start",t_start_lin)
print("stop",t_stop_lin)
print("full",sub_pulse_times)
