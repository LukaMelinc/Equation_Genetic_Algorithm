% Parametri TS modela
R = 10; % Število podfunkcij
C = rand(R, 2);  % Centri funkcij
O = rand(R, 1);  % Širine podfunkcij
W = rand(R, 4);  % Uteži linearnih funkcij
b = rand(R, 1);  % Biasi linearnih funkcij
learning_rate = 0.001; % Learning rate
epochs = 200; % Število učnih epoh

% Membership funckija pove, koliko posamezno pravilo doprinese k končnemu
% izhodu funkcije

% trening TS modela
[C, O, W, b] = TS_train(C, O, W, b, X_shifted, Y_shifted, learning_rate, epochs);


% Napovedan izhod modela
%Y_predicted = TS_eval(C, O, W, b, X_test');

Y_simulated = zeros(size(Y_test));
for i = 1:length(Y_test)
    if i == 1
        y_prev1 = y_test(i+1); % y_test(2)
        y_prev2 = y_test(i);   % y_test(1)
    elseif i == 2
        y_prev1 = Y_simulated(i-1); % Y_simulated(1) which predicts y_test(3)
        y_prev2 = y_test(i);        % y_test(2)
    else
        y_prev1 = Y_simulated(i-1);
        y_prev2 = Y_simulated(i-2);
    end

    % Construct the input vector
    x_current = [u_test(i+1), u_test(i), -y_prev1, -y_prev2];

    % Predict the current output
    y_predicted_current = TS_eval(C, O, W, b, x_current');

    % Store the predicted output
    Y_simulated(i) = y_predicted_current;
end


% MAE TS modela
mae_ts = mean(abs(Y_test - Y_simulated'));
fprintf('Takagi-Sugeno Model MAE: %.4f\n', mae_ts);


% Primejrava dejanskega in napovedanega izhoda
figure('Position', [100, 100, 1200, 800]);

plot(Y_test);
hold on;
plot(Y_simulated);

title('Primerjava napovedanega in dejanskega izhoda (TS)');
xlabel('Sample');
ylabel('Vrednotst izhoda [V]');
legend('Dejanski izhod', 'Napovedan izhod modela');
grid on;
hold off;