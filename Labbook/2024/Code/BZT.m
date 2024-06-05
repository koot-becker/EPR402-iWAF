
format long
base = 522e3;
ch = zeros(1, 120);


for x = 1:120
    ch(x) = (base + x * 9e3);  
end

Fs = 3230769;
FN = Fs/2;

output = "{";

for z=1:120
    f0 = ch(z);
    
    fp1 = f0 - 4.5e3;
    fp2 = f0 + 4.5e3;
    fs1 = f0 - 6.3e3;
    fs2 = f0 + 6.3e3;


    [A, B, C, D] = butter(6,[fp1 fp2]/FN);

    sos = ss2sos(A,B,C,D);


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
    if z == 1
        output = output + xport;
    else
        output = output + ", " + xport;
    end
end

output = output + "}";
output

fileID = fopen('channels.txt', 'wt');
fprintf(fileID, output);
fclose(fileID);

[b, a] = butter(6,[fp1 fp2]/FN);
fvt = fvtool(sos,'Fs',Fs);
legend(fvt,'butter')
