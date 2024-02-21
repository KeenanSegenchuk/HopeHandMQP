function user = checkUserCommand(ivs, afe, audio, fs)
%CHECKSPEAKERCOMMAND Summary of this function goes here
%   return true if a user enrolled in ivs has spoken for less than half a
%   second
    user = verifySpeaker(audio,ivs,afe) & checkCommand(audio, fs);
end

