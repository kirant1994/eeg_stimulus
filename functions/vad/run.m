clc;
clear;

path = 'audio/mobile';
filelist = dir(path);

for i = 3:length(filelist)
    tmp = filelist(i).name;
    st = max(length(tmp)-3, 1);
    en = length(tmp);
    if strcmp(tmp(st:en), '.wav')
        name = filelist(i).name(1:end-4);
        inname = sprintf('%s/%s.wav', path, name);
        outname = sprintf('%s/%s_vad.wav', path, name);
        outtxt = sprintf('%s/%s_vad.txt', path, name);
        vad(inname, '', outtxt, 0.1, outname);
    end
end