function user = verifySpeaker(audio, ivs)
%   return true if the audio is from a user enrolled in
    disp("1")
    %certainty threshold for accepting audio as being from user 
    threshold = .177;

    results = identify(ivs,audio,"plda");

    if results.Score(1) < threshold
        user = true;
    else
        user = false;
    end
end

