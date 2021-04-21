limit = 5
my_list = [89, 47, 52, 58, 96, 45, 25, 74, 12, 36, 74]
i = 0
moving_averages_values = []

while i < len(my_list) - limit + 1:
    values = my_list[i : i + limit]

    moving_average = sum(values) / limit
    moving_averages_values.append(moving_average)
    i += 1

    print(moving_average)
# for i in range (len(moving_averages_values)):
#     
#     print(moving_averages_values[i])
#     p