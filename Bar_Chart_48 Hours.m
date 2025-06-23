% CONFIGURATION
channelID = YOUR_CHANNEL_ID;         
readAPIKey = 'YOUR_READ_API_KEY';    
VAT = 0.19;                          % VAT percentage (19% for Germany)

% FETCH DATA Numpoints 48 = 48 hours 
data = thingSpeakRead(channelID, ...
    'NumPoints', 48, ...
    'Fields', [1,2], ...  % Field 1 = Consumption (kWh), Field 2 = Cost (EUR)
    'ReadKey', readAPIKey);

consumption = data(:,1);
cost = data(:,2) * (1 + VAT);   % Cost with VAT

% FETCH TIMESTAMPS Numpoints 48 = 48 hours 
timestamps = thingSpeakRead(channelID, 'NumPoints', 48, 'ReadKey', readAPIKey, 'OutputFormat', 'timetable');
time = timestamps.Timestamps;

% CREATE BAR CHART
figure;
bar(time, consumption, 'FaceColor', [0.2 0.6 0.8]);
xlabel('Time');
ylabel('Consumption (kWh)');
title('Electricity Consumption - Last 48 Hours');
grid on;

% COST ABOVE EACH BAR
hold on;
for i = 1:length(cost)
    text(time(i), consumption(i) + 0.02, sprintf('€%.2f', cost(i)), ...
        'Rotation', 90, 'HorizontalAlignment', 'center', 'FontSize', 8);
end
hold off;

% FORMAT X-TICKS
xtickformat('HH:mm dd/MM');
xtickangle(45);

