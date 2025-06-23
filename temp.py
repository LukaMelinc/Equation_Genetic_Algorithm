function [A_state, B_state, C_state, R_state] = Convert(centers, spreads, weights, offsets, input)

    % Prevajanje TS modela v prostor stanj

    numRules = size(centers, 1);  % Število funkcij
    [A_state, B_state, C_state, R_state] = deal(zeros(2, 2), zeros(2, 1), zeros(1, 2), zeros(2, 1));

    membershipValues = exp(-0.5 * sum((input' - centers).^2 ./ (spreads.^2), 2));  % Gaussian membership
    membershipValues = membershipValues / sum(membershipValues);  % Normalizcija membershipov

    % Sestavitev matrik stanja
    for ruleIndex = 1:numRules
        A_rule = [0, -weights(ruleIndex, 4); 1, -weights(ruleIndex, 3)];  % 2x2, uteži po diagonali -> Dinamika sistema
        B_rule = [weights(ruleIndex, 2); weights(ruleIndex, 1)]; % 2x1 -> vpliv vhoda na stanje
        C_rule = [0, 1];
        R_rule = [0; offsets(ruleIndex)];  % Deviacija dinamike za funkcijo

        % Posodobitev matrik prostora stanj za posamezno pravilo
        A_state = A_state + membershipValues(ruleIndex) * A_rule;
        B_state = B_state + membershipValues(ruleIndex) * B_rule;
        C_state = C_state + membershipValues(ruleIndex) * C_rule;
        R_state = R_state + membershipValues(ruleIndex) * R_rule;
    end
    input=0;
    
end