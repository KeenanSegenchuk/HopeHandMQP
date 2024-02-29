function user = verifySpeaker(audio, ivs)
%   return true if the audio is from a user enrolled in

    %certainty threshold for accepting audio as being from user 
    threshold = 1 - .177;

    results = identify(ivs,audio,"plda");
    disp(results.Score(1))
    if results.Score(1) > threshold
        user = true;
    else
        user = false;
    end
end

