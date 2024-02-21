function user = verifySpeaker(audio, ivs, afe)
%   return true if the audio is from a user enrolled in
    
    %certainty threshold for accepting audio as being from user 
    threshold = .9;

    features = extract(afe,audio);
    results = identify(ivs,features,"plda");

    if results.Score(1) < threshold
        user = true;
    else
        user = false;
    end
end

