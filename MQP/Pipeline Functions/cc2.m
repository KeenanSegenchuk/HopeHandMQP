function command = cc2(audio, fs)
%   Check if speech in audio is the length of a single word
    command = true;
    audio(abs(audio)<.01) = 0;

    windowDuration = 0.045; % seconds
    numWindowSamples = round(windowDuration*fs);
    win = hamming(numWindowSamples,'periodic');
    
    percentOverlap = 35;
    overlap = round(numWindowSamples*percentOverlap/100);
    
    mergeDuration = 0.24;
    mergeDist = round(mergeDuration*fs);
    
    idx = detectSpeech(audio,fs,"Window",win,"OverlapLength",overlap,"MergeDistance",mergeDist);
    %check for no commands
    if isempty(idx)
        command = false;
    end
    disp(idx)
    %check for ongoing speech
    for i = 1:size(idx, 1)
        if idx(i, 2) - idx(i,1) > fs*3/4
            command = false;
        end
    end
end
