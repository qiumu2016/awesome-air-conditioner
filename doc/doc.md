# administrator

## power_on

request:

return: 

| key   | 描述 |
| ----- | ---- |
| state | ok   |

## set_para

request:

| key                 | 描述               |
| ------------------- | ------------------ |
| model               | hot/cold           |
| temp_high_limit     | 数字 最低温度      |
| temp_low_limit      | 数字 最低温度      |
| default_target_temp | 默认目标温度       |
| fee_rate_h          | 高风速费率         |
| fee_rate_m          | 中风速费率         |
| fee_rate_l          | 低风速费率         |
| num_rooms           | 房间数             |
| num_serve           | 对多同时服务房间数 |

return: 

| key   | 描述 |
| ----- | ---- |
| state | ok   |

## start_up

request:

return: 

| key   | 描述 |
| ----- | ---- |
| state | ok   |

## check_room_state

request：

| key     | 描述       |
| ------- | ---------- |
| room_id | 房间号数字 |

return：

| key   | 描述        |
| ----- | ----------- |
| isCheckIn | 是否入住 0：否 1：是 |
| isOpen | 是否开机 0：否 1：是 |
| isServing | 是否正在服务 0：否 1：是 |
| wind | 风速：high/mid/low |
| current_temp | 当前温度 |
| target_temp | 目标温度 |
| fee_rate | 当前费率 |
| fee | 当前费用 |

# desk

## print_rdr

request：

| key     | 描述       |
| ------- | ---------- |
| room_id | 房间号数字 |

return:

一个文件 直接被下载

## print_invoice

request：

| key     | 描述       |
| ------- | ---------- |
| room_id | 房间号数字 |

return:

一个文件 直接被下载

# manager

## print_report

request：

| key  | 描述                      |
| ---- | ------------------------- |
| type | day / week / month / year |

return:

一个文件 直接被下载

# costumer

## request_on

request：

| key               | 描述          |
| ----------------- | ------------- |
| room_id           | 房间编号 数字 |
| current_room_temp | 当前房间温度  |

return

| key         | 描述     |
| ----------- | -------- |
| model       | cold/hot |
| target_temp | 目标温度 |

## request_off

request：

| key               | 描述          |
| ----------------- | ------------- |
| room_id           | 房间编号 数字 |
| current_room_temp | 当前房间温度  |

return

| key   | 描述 |
| ----- | ---- |
| state | ok   |

## change_target_temp

request：

| key         | 描述          |
| ----------- | ------------- |
| room_id     | 房间编号 数字 |
| target_temp | 当前房间温度  |

return:

| key   | 描述 |
| ----- | ---- |
| state | ok   |

## change_fan_speed

request：

| key       | 描述          |
| --------- | ------------- |
| room_id   | 房间编号 数字 |
| fan_speed | high/mid/low  |

return:

| key   | 描述 |
| ----- | ---- |
| state | ok   |

## request_info

request：

| key     | 描述       |
| ------- | ---------- |
| room_id | 房间号数字 |

return：

| key          | 描述                     |
| ------------ | ------------------------ |
| isCheckIn    | 是否入住 0：否 1：是     |
| isOpen       | 是否开机 0：否 1：是     |
| isServing    | 是否正在服务 0：否 1：是 |
| wind         | 风速：high/mid/low       |
| current_temp | 当前温度                 |
| fee_rate     | 当前费率                 |
| fee          | 当前费用                 |