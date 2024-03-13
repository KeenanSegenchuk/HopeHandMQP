function user = verifySpeaker(audio, fs, ivs, afe)
%   return true if the audio is from a user enrolled in

    %resample audio to same rate as audio feature extractor
    afe_fs = 32e3;
    resample(audio, afe_fs, fs);

    %certainty threshold for accepting audio as being from user 
    threshold = .85;

    results = identify(ivs,extract(afe, audio),"plda");
    disp(results.Score(1))
    if results.Score(1) > threshold
        user = true;
    else
        user = false;
    end
end