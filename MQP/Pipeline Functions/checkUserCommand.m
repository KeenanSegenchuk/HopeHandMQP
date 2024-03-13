function user  = checkUserCommand(ivs, afe, audio, fs)
%CHECKSPEAKERCOMMAND Summary of this function goes here
%   return true if a user enrolled in ivs has spoken for less than half a
%   second
    audio = double(audio)';
    fs = double(fs);
    speaker = verifySpeaker(audio,fs,ivs,afe);
    disp("User recognized: ");
    disp(speaker);
    command = cc2(audio, fs);
    disp("Command Recognized: ");
    disp(command);
    user = speaker & command;
    user = [speaker, command, user];
end

