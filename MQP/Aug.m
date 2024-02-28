classdef Aug
    %AUG: static class containing a bunch of functions for augmenting audio
    %data


    methods(Static)
        function a_a = speedup(audio, fs, speedupfactor)
            aug = audioDataAugmenter('AugmentationParameterSource','specify', ...
                 'ApplyTimeStretch',true, ...
                 'SpeedupFactor', speedupfactor);
            a_a = augment(aug, audio, fs).Audio{:};
            sound(a_a, fs);
        end

        function a_a = pitchshift(audio, fs, toneshift)
            aug = audioDataAugmenter('AugmentationParameterSource','specify', ...
                 'ApplyPitchShift',true, ...
                 'SemitoneShift', toneshift);
            a_a = augment(aug, audio, fs).Audio{:};
            sound(a_a, fs);
        end

        function a_a = volumeshift(audio, fs, gain)
            aug = audioDataAugmenter('AugmentationParameterSource','specify', ...
                 'ApplyVolumeControl',true, ...
                 'VolumeGain', gain);
            a_a = augment(aug, audio, fs).Audio{:};
            sound(a_a, fs);
        end

        function a_a = addnoise(audio, fs, SNR)
            %SNR is ratio of input audio signal to added noise
            aug = audioDataAugmenter('AugmentationParameterSource','specify', ...
                 'ApplyAddNoise',true, ...
                 'SNR', SNR);
            a_a = augment(aug, audio, fs).Audio{:};
            sound(a_a, fs);
        end

        function aug = getAugmenter(speedup, toneshift, gain, SNR, mode, params, numAugs, probabilities)
            %SNR is ratio of input audio signal to added noise
            %MODE can be "sequential" or "independent"
                %"sequential" applies every combination of augments
                %togeether which produces length(speedup) *
                %length(toneshift) * length(gain) * length(SNR) output
                %signals
                %
                %"independent" applies each augment to a seperate signal 
                % which produces length(speedup) + length(toneshift) +
                % ength(gain) + length(SNR) output signals
            %PARAMS can be "random" or "specify"
                %"specify" applies augment deterministically with every
                %value in arrays speedup, toneshift, gain, SNR
                %
                %"random" requires numAugs and probabilities and it 
                %randomly applies augments in the range specified by the
                %tuples speedup, toneshift, gain, SNR
            %PROBABILITIES must be an array of length 4 and gives the
            %probablilities of applying speedup, toneshift, volumengain,
            %and adding noise (SNR) in a range of 0 to 1. For "specify" the
            %array should only contain 1s or 0s which tells it to apply
            %that augment or not
            %NUMAUGS tells how many random augments to apply

            if strcmp(params, "random")
                aug = audioDataAugmenter( ...
                    "AugmentationMode", mode, ...
                    "NumAugmentations",numAugs, ...
                    ...
                    "TimeStretchProbability",probabilities(1), ...
                    "SpeedupFactorRange", speedup, ...
                    ...
                    "PitchShiftProbability",probabilities(2), ...
                    "SemitoneShiftRange", toneshift, ...
                    ...
                    "VolumeControlProbability",probabilities(3), ...
                    "VolumeGainRange",gain, ...
                    ...
                    "AddNoiseProbability", probabilities(4), ...
                    "SNRRange", SNR);
            else   
                aug = audioDataAugmenter( ...
                    "AugmentationMode", mode, ...
                    "AugmentationParameterSource","specify", ...
                    ...
                    "ApplyTimeStretch",probabilities(1), ...
                    "SpeedupFactor", speedup, ...
                    ...
                    "ApplyPitchShift",probabilities(2), ...
                    "SemitonShift", toneshift, ...
                    ...
                    "ApplyVolumeControl",probabilities(3), ...
                    "VolumeGain",gain, ...
                    ...
                    "ApplyAddNoise", probabilities(4), ...
                    "SNR", SNR);
            end
        end

        function augmentFolder(aug, inputfolder, outputfolder, classes)
            %use audioDataAugmenter aug to augment database at location
            %inputfolder with subfolders classes and save augmented
            %database to outputfolder
            if ~exist(outputfolder, "dir")
                mkdir(outputfolder);
            end

            for class = 1:length(classes)
                path = inputfolder + "\" + classes(class);
                filenames = dir(path);
                filenames = filenames(3:length(filenames));

                if ~exist(outputfolder + "\" + classes(class), "dir")
                    mkdir(outputfolder + "\" + classes(class));
                end

                for file = 1:length(filenames)
                    [a, fs] = audioread(path + "\" + filenames(file).name);
                    a_a = augment(aug, a, fs).Audio{:};
                    audiowrite(outputfolder + "\" + classes(class) + "\" +  filenames(file).name, a_a, fs);
                end
            end
        end
    end
end









