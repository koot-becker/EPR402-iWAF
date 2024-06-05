
format long
f0 = 1366e3;
Fs = 3230769;
FN = Fs/2;

fp1 = f0 - 4.5e3;
fp2 = f0 + 4.5e3;
fs1 = f0 - 6.3e3;
fs2 = f0 + 6.3e3;


[A, B, C, D] = butter(6,[fp1 fp2]/FN);
[b, a] = butter(6,[fp1 fp2]/FN);

sos = ss2sos(A,B,C,D);
fvt = fvtool(sos,'Fs',Fs);
legend(fvt,'butter')

xport = "{";
for x = 1:6
    for y = 1:3
        if (x == 1) && (y == 1)
            xport = xport + num2str(sos(x,y), 14);
        else
            xport = xport + ", " + num2str(sos(x,y), 14);
        end
    end
    for y = 5:6
        xport = xport + ", " + num2str(-1 * sos(x,y), 14);
    end
end
xport = xport + "}";


