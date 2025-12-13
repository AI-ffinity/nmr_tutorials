These extra empty spaces along the direct dimension in the 15N-HSQC could be reduced by shortening the spectral width
of the direct dimension, but that will have minimal effect on the total acquisition time. That’s because along the 
direct dimension, the acquisition runs in real time. If it was along an indirect dimension, like nitrogen in this 
spectrum, then for every TD point it measures again, and therefore, if we remove TD points along the indirect dimension, 
we reduce the acquisition time. For example, if we remove half of the TD points along the 15N dimension, then we reduce 
the acquisition time almost by half. On the other hand, if you reduce the TD points to half along the direct dimension, 
then you save around 10 milliseconds per point—so multiplied by 256, it’s about half a minute time-saving for an HSQC 
for quality control.

Further optimization of these parameters is not necessary. It will be necessary if we measure a 3D or 4D experiment. 
More than by the values of the parameter TD, the total acquisition time is affected at most by the parameter 
D1 (relaxation delay: 1–5 × T1). In the best HSQC pulse sequence, the value of D1 is shorter, but we measure more scans. 
BEST is a special method that exploits the effect of the magnetization of the water signal in order for the protein 
magnetization to return—that’s why D1 is so short. Otherwise, it’s usually set to one second or higher.

I stopped the video at 2:48