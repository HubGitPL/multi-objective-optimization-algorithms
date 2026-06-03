classdef NSGAII_Roul < ALGORITHM
% <2026> <multi> <real/integer/label/binary/permutation> <constrained/none>
% NSGA-II variant with roulette-wheel selection.
% Mating selection uses RouletteWheelSelection with FrontNo as the only
% fitness value (no crowding distance in the mating selection).
% Environmental selection (truncation to N) is kept as in original NSGA-II.

    methods
        function main(Algorithm,Problem)
            %% Generate random population
            Population = Problem.Initialization();
            [~,FrontNo,CrowdDis] = EnvSelection_Roul(Population,Problem.N);

            %% Optimization loop
            while Algorithm.NotTerminated(Population)
                % Roulette-wheel selection with FrontNo as fitness.
                % In RouletteWheelSelection smaller fitness => larger
                % probability, which matches our case (FrontNo=1 is best).
                MatingPool = RouletteWheelSelection(Problem.N,FrontNo);
                Offspring  = OperatorGA(Problem,Population(MatingPool));
                [Population,FrontNo,CrowdDis] = EnvSelection_Roul([Population,Offspring],Problem.N);
            end
        end
    end
end
