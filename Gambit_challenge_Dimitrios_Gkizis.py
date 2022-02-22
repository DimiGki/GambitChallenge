"""This application is the solution to the Gambit Challenge with 
the TUF-2000M sensor.

It reads data from a given URL, converts them so that a person can read 
them and dislpays them in two ways. The first through the terminal and
the second with the use of an interface, made with the tkinter module.

It also creates an XML file (data.xml) with the data created so that they can be displayed
using an html file."""
import struct
import requests
from tkinter import *
from tkinter import ttk
import xml.etree.ElementTree as xml


def convert_decs_to_bins(dec1, dec2):
    """Converts decimals to binaries and combines them"""
    bin1 = twosCom_decBin(int(dec1), 16)
    bin2 = twosCom_decBin(int(dec2), 16)
    return bin2 + bin1


def twosCom_decBin(dec, digit):
    """Converts a decimal to binary
        
    source ->
    https://cysecguide.blogspot.com/2017/12/converting-binarydecimal-of-twos.html"""
    if dec>=0:
        bin1 = bin(dec).split("0b")[1]
        while len(bin1)<digit :
            bin1 = '0'+bin1
        return bin1
    else:
        bin1 = -1*dec
        return bin(dec-pow(2,digit)).split("0b")[1]

            
def twosCom_binDec(bin, digit):
    """Converts a binary to decimal"""
    while len(bin)<digit :
        bin = '0'+bin
    if bin[0] == '0':
        return int(bin, 2)
    else:
        return -1 * (int(''.join('1' if x == '0' else '0' for x in bin), 2) + 1)


def adjust_decimals(value):
    """Adjusts the decimals of a value to 4"""
    return f'{value:.4f}'


# Reading the data from the url
data = requests.get('http://tuftuf.gambitlabs.fi/feed.txt')
# print(data.text)
# data is in response type and data.text is in string type


# Converting data to list
data_list = list(data.text.splitlines())
# print(data_list, '\n')


# Striping the list from the numbers
data_list_striped = []
for item in range (len(data_list)):
    index = data_list[item].find(':')
    data_list_striped.append(data_list[item][(index + 1):])
    # print(data_list[item][(index + 1):])
# print(data_list_striped)


# Creating the xml file
root = xml.Element('data')


# reg 1-2 real4
reg1_2 = convert_decs_to_bins(data_list_striped[1], data_list_striped[2])
reg1_2_value = struct.unpack("f", struct.pack("L", int(reg1_2,2)))[0]
# Adjusting the decimals of the measurement
reg1_2_value = adjust_decimals(reg1_2_value)
# Adding the value as a XML tag
flow_rate = xml.SubElement(root, 'flow_rate')
flow_rate.text = reg1_2_value
# Printing the value to the terminal
print('Flow Rate: ', reg1_2_value, u'm\u00B3/h')

# reg 3-4 real4
reg3_4 = convert_decs_to_bins(data_list_striped[3], data_list_striped[4])
reg3_4_value = struct.unpack("f", struct.pack("L", int(reg3_4,2)))[0]
reg3_4_value = adjust_decimals(reg3_4_value)
energy_flow_rate = xml.SubElement(root, 'energy_flow_rate')
energy_flow_rate.text = reg3_4_value
print('Energy Flow Rate: ', reg3_4_value, 'GJ/h')

# reg 5-6 real4
reg5_6 = convert_decs_to_bins(data_list_striped[5], data_list_striped[6])
reg5_6_value = struct.unpack("f", struct.pack("L", int(reg5_6,2)))[0]
reg5_6_value = adjust_decimals(reg5_6_value)
velocity = xml.SubElement(root, 'velocity')
velocity.text = reg5_6_value
print('Velocity: ', reg5_6_value, 'm/s')

# reg 7-8 real4
reg7_8 = convert_decs_to_bins(data_list_striped[7], data_list_striped[8])
reg7_8_value = struct.unpack("f", struct.pack("L", int(reg7_8,2)))[0]
reg7_8_value = adjust_decimals(reg7_8_value)
fluid_sound_speed = xml.SubElement(root, 'fluid_sound_speed')
fluid_sound_speed.text = reg7_8_value
print('Fluid sound speed: ', reg7_8_value, 'm/s')

# reg 9-10 long
reg9_10 = convert_decs_to_bins(data_list_striped[9], data_list_striped[10])
reg9_10_value = twosCom_binDec(reg9_10, 32)
positive_accumulator = xml.SubElement(root, 'positive_accumulator')
# Longs must be converted to str or else error occures
positive_accumulator.text = str(reg9_10_value)
print('Positive accumulator: ', reg9_10_value)

# reg 11-12 real4
reg11_12 = convert_decs_to_bins(data_list_striped[11], data_list_striped[12])
reg11_12_value =  struct.unpack("f", struct.pack("L", int(reg11_12,2)))[0]
reg11_12_value = adjust_decimals(reg11_12_value)
positive_decimal_fraction = xml.SubElement(root, 'positive_decimal_fraction')
positive_decimal_fraction.text = reg11_12_value
print('Positive decimal fraction: ', reg11_12_value)

# reg 13-14 long
reg13_14 = convert_decs_to_bins(data_list_striped[13], data_list_striped[14])
reg13_14_value = twosCom_binDec(reg13_14, 32)
negative_accumulator = xml.SubElement(root, 'negative_accumulator')
negative_accumulator.text = str(reg13_14_value)
print('Negative accumulator: ', reg13_14_value)

# reg 15-16 real4
reg15_16 = convert_decs_to_bins(data_list_striped[15], data_list_striped[16])
reg15_16_value = struct.unpack("f", struct.pack("L", int(reg15_16,2)))[0]
reg15_16_value = adjust_decimals(reg15_16_value)
negative_decimal_fraction = xml.SubElement(root, 'negative_decimal_fraction')
negative_decimal_fraction.text = reg15_16_value
print('Negative decimal fraction: ', reg15_16_value)

# reg 17-18 long
reg17_18 = convert_decs_to_bins(data_list_striped[17], data_list_striped[18])
reg17_18_value = twosCom_binDec(reg17_18, 32)
positive_energy_accumulator = xml.SubElement(root, 'positive_energy_accumulator')
positive_energy_accumulator.text = str(reg17_18_value)
print('Positive energy accumulator: ', reg17_18_value)

# reg 19-20 real4
reg19_20 = convert_decs_to_bins(data_list_striped[19], data_list_striped[20])
reg19_20_value = struct.unpack("f", struct.pack("L", int(reg19_20,2)))[0]
reg19_20_value = adjust_decimals(reg19_20_value)
positive_energy_decimal_fraction = xml.SubElement(root, 'positive_energy_decimal_fraction')
positive_energy_decimal_fraction.text = reg19_20_value
print('Positive energy decimal fraction: ', reg19_20_value)

# reg 21-22, type LONG
reg21_22 = convert_decs_to_bins(data_list_striped[21], data_list_striped[22])
reg21_22_value = twosCom_binDec(reg21_22, 32)
negative_energy_accumulator = xml.SubElement(root, 'negative_energy_accumulator')
negative_energy_accumulator.text = str(reg21_22_value)
print('Negative energy accumulator: ', reg21_22_value)

# reg 23-24 real4
reg23_24 = convert_decs_to_bins(data_list_striped[23], data_list_striped[24])
reg23_24_value = struct.unpack("f", struct.pack("L", int(reg23_24,2)))[0]
reg23_24_value = adjust_decimals(reg23_24_value)
negative_energy_decimal_fraction = xml.SubElement(root, 'negative_energy_decimal_fraction')
negative_energy_decimal_fraction.text = reg23_24_value
print('Negative energy decimal fraction: ', reg23_24_value)

# reg 25-26 long
reg25_26 = convert_decs_to_bins(data_list_striped[25], data_list_striped[26])
reg25_26_value = twosCom_binDec(reg25_26, 32)
net_accumulator = xml.SubElement(root, 'net_accumulator')
net_accumulator.text = str(reg25_26_value)
print('Net accumulator: ', reg25_26_value)

# reg 27-28 real4
reg27_28 = convert_decs_to_bins(data_list_striped[27], data_list_striped[28])
reg27_28_value = struct.unpack("f", struct.pack("L", int(reg27_28,2)))[0]
reg27_28_value = adjust_decimals(reg27_28_value)
net_decimal_fraction = xml.SubElement(root, 'net_decimal_fraction')
net_decimal_fraction.text = reg27_28_value
print('Net decimal fraction: ', reg27_28_value)

# reg 29-30 long
reg29_30 = convert_decs_to_bins(data_list_striped[29], data_list_striped[30])
reg29_30_value = twosCom_binDec(reg29_30, 32)
net_energy_accumulator = xml.SubElement(root, 'net_energy_accumulator')
net_energy_accumulator.text = str(reg29_30_value)
print('Net energy accumulator: ', reg29_30_value)

# reg 31-32 real4
reg31_32 = convert_decs_to_bins(data_list_striped[31], data_list_striped[32])
reg31_32_value = struct.unpack("f", struct.pack("L", int(reg31_32,2)))[0]
reg31_32_value = adjust_decimals(reg31_32_value)
net_energy_decimal_fraction = xml.SubElement(root, 'net_energy_decimal_fraction')
net_energy_decimal_fraction.text = reg31_32_value
print('Net energy decimal fraction: ', reg31_32_value)

# reg 33-34 real4
reg33_34 = convert_decs_to_bins(data_list_striped[33], data_list_striped[34])
reg33_34_value = struct.unpack("f", struct.pack("L", int(reg33_34,2)))[0]
reg33_34_value = adjust_decimals(reg33_34_value)
temperature1 = xml.SubElement(root, 'temperature1')
temperature1.text = reg33_34_value
print('Temperature #1/inlet: ', reg33_34_value, 'C')

# reg 35-36 real4
reg35_36 = convert_decs_to_bins(data_list_striped[35], data_list_striped[36])
reg35_36_value = struct.unpack("f", struct.pack("L", int(reg35_36,2)))[0]
reg35_36_value = adjust_decimals(reg35_36_value)
temperature2 = xml.SubElement(root, 'temperature2')
temperature2.text = reg35_36_value
print('Temperature #2/outlet: ', reg35_36_value, 'C')

# reg 37-38 real4
reg37_38 = convert_decs_to_bins(data_list_striped[37], data_list_striped[38])
reg37_38_value = struct.unpack("f", struct.pack("L", int(reg37_38,2)))[0]
reg37_38_value = adjust_decimals(reg37_38_value)
analog_input_AI3 = xml.SubElement(root, 'analog_input_AI3')
analog_input_AI3.text = reg37_38_value
print('Analog input AI3: ', reg37_38_value)

# reg 39-40 real4
reg39_40 = convert_decs_to_bins(data_list_striped[39], data_list_striped[40])
reg39_40_value = struct.unpack("f", struct.pack("L", int(reg39_40,2)))[0]
reg39_40_value = adjust_decimals(reg39_40_value)
analog_input_AI4 = xml.SubElement(root, 'analog_input_AI4')
analog_input_AI4.text = reg39_40_value
print('Analog input AI4: ', reg39_40_value)

# reg 41-42 real4
reg41_42 = convert_decs_to_bins(data_list_striped[41], data_list_striped[42])
reg41_42_value = struct.unpack("f", struct.pack("L", int(reg41_42,2)))[0]
reg41_42_value = adjust_decimals(reg41_42_value)
analog_input_AI5 = xml.SubElement(root, 'analog_input_AI5')
analog_input_AI5.text = reg41_42_value
print('Analog input AI5: ', reg41_42_value)

# reg 43-44 real4
reg43_44 = convert_decs_to_bins(data_list_striped[43], data_list_striped[44])
reg43_44_value = struct.unpack("f", struct.pack("L", int(reg43_44,2)))[0]
reg43_44_value = adjust_decimals(reg43_44_value)
current_input_AI3_1 = xml.SubElement(root, 'current_input_AI3_1')
current_input_AI3_1.text = reg43_44_value
print('Current input AI3: ', reg43_44_value, 'mA')

# reg 45-46 real4
reg45_46 = convert_decs_to_bins(data_list_striped[45], data_list_striped[46])
reg45_46_value = struct.unpack("f", struct.pack("L", int(reg45_46,2)))[0]
reg45_46_value = adjust_decimals(reg45_46_value)
current_input_AI3_2 = xml.SubElement(root, 'current_input_AI3_2')
current_input_AI3_2.text = reg43_44_value
print('Current input AI3: ', reg45_46_value, 'mA')

# reg 47-48 real4
reg47_48 = convert_decs_to_bins(data_list_striped[47], data_list_striped[48])
reg47_48_value = struct.unpack("f", struct.pack("L", int(reg47_48,2)))[0]
reg47_48_value = adjust_decimals(reg47_48_value)
current_input_AI3_3 = xml.SubElement(root, 'current_input_AI3_3')
current_input_AI3_3.text = reg47_48_value
print('Current input AI3: ', reg47_48_value, 'mA')

# reg 49-50 bcd (binary coded decimal)
# 7 digit password
reg49_50 = convert_decs_to_bins(data_list_striped[49], data_list_striped[50])
reg49_50 = str(twosCom_binDec(reg49_50[0:4],8)) \
+ str(twosCom_binDec(reg49_50[4:8],8)) + str(twosCom_binDec(reg49_50[8:12],8)) \
+ str(twosCom_binDec(reg49_50[12:16],8)) + str(twosCom_binDec(reg49_50[16:20],8)) \
+ str(twosCom_binDec(reg49_50[20:24],8)) + str(twosCom_binDec(reg49_50[24:28],8))
system_password = xml.SubElement(root, 'system_password')
system_password.text = reg49_50
print('System Password: ', reg49_50)

# reg 51 bcd
# 4 digit password
reg51 = twosCom_decBin(int(data_list_striped[51]), 16)
reg51 = str(twosCom_binDec(reg51[0:4],8)) \
+ str(twosCom_binDec(reg51[4:8],8)) + str(twosCom_binDec(reg51[8:12],8)) \
+ str(twosCom_binDec(reg51[12:16],8))
password_for_hardware = xml.SubElement(root, 'password_for_hardware')
password_for_hardware.text = reg51
print('Password for hardware: ', reg51)

# reg 53-55 bcd
reg53 = twosCom_decBin(int(data_list_striped[53]), 16)
reg54 = twosCom_decBin(int(data_list_striped[54]), 16)
reg55 = twosCom_decBin(int(data_list_striped[55]), 16)

reg53_55 = reg55 + reg54 + reg53

year = str(twosCom_binDec(reg53_55[0:4],8)) + str(twosCom_binDec(reg53_55[4:8],8))
month = str(twosCom_binDec(reg53_55[8:12],8)) + str(twosCom_binDec(reg53_55[12:16],8))
day = str(twosCom_binDec(reg53_55[16:20],8)) + str(twosCom_binDec(reg53_55[20:24],8))
hour = str(twosCom_binDec(reg53_55[24:28],8)) + str(twosCom_binDec(reg53_55[28:32],8))
minute = str(twosCom_binDec(reg53_55[32:36],8)) + str(twosCom_binDec(reg53_55[36:40],8))
sec = str(twosCom_binDec(reg53_55[40:44],8)) + str(twosCom_binDec(reg53_55[44:48],8))
date = year + '/' + month + '/' + day + ',' + hour + ':' + minute + ':' + sec

date_xml = xml.SubElement(root, 'date')
date_xml.text = date

print('Date: ', year, '/', month, '/', day, ', ', hour, ':', minute, ':', sec, sep='')

# reg 56 bcd
# 4 digits 2 for the day 2 for the hour
reg56 = twosCom_decBin(int(data_list_striped[56]), 16)
day_autosave = str(twosCom_binDec(reg56[0:4],8)) + str(twosCom_binDec(reg56[4:8],8))
hour_autosave = str(twosCom_binDec(reg56[8:12],8)) + str(twosCom_binDec(reg56[12:16],8))
reg56 = day_autosave + hour_autosave
day_hour_autosave = xml.SubElement(root, 'day_hour_autosave')
day_hour_autosave.text = reg56
print('Day + hour for Autosave: ', reg56)

# reg 59 integer
reg59 = data_list_striped[59]
key_to_input = xml.SubElement(root, 'key_to_input')
key_to_input.text = reg59
print('Key to input: ', reg59)

# reg 60 integer
reg60 = data_list_striped[60]
go_to_window = xml.SubElement(root, 'go_to_window')
go_to_window.text = reg60
print('Go to Window #: ', reg60)

# reg 61 integer
reg61 = data_list_striped[61]
LCD_back_lit_lights_seconds = xml.SubElement(root, 'LCD_back_lit_lights_seconds')
LCD_back_lit_lights_seconds.text = reg61
print('LCD Back-lit lights for number of seconds: ', reg61, 'sec')

# reg 62 integer
reg62 = data_list_striped[62]
times_for_the_beeper = xml.SubElement(root, 'times_for_the_beeper')
times_for_the_beeper.text = reg62
print('Times for the beeper: ', reg62)
print('Pulses left for OCT: ', reg62)

# reg 72 bit
reg72 = twosCom_decBin(int(data_list_striped[72]), 16)
error_code = xml.SubElement(root, 'error_code')
error_code.text = reg72
print('Error code: ', reg72)

# reg 77-78 real4
reg77_78 = convert_decs_to_bins(data_list_striped[77], data_list_striped[78])
reg77_78_value = struct.unpack("f", struct.pack("L", int(reg47_48,2)))[0]
reg77_78_value = adjust_decimals(reg77_78_value)
PT100_resistance_of_inlet = xml.SubElement(root, 'PT100_resistance_of_inlet')
PT100_resistance_of_inlet.text = reg77_78_value
print('PT100 resistance of inlet: ', reg77_78_value, 'Ohm')

# reg 79-80 real4
reg79_80 = convert_decs_to_bins(data_list_striped[79], data_list_striped[80])
reg79_80_value = struct.unpack("f", struct.pack("L", int(reg79_80,2)))[0]
reg79_80_value = adjust_decimals(reg79_80_value)
PT100_resistance_of_outlet = xml.SubElement(root, 'PT100_resistance_of_outlet')
PT100_resistance_of_outlet.text = reg79_80_value
print('PT100 resistance of outlet: ', reg79_80_value, 'Ohm')

# reg 81-82 real4
reg81_82 = convert_decs_to_bins(data_list_striped[81], data_list_striped[82])
reg81_82_value = struct.unpack("f", struct.pack("L", int(reg81_82,2)))[0]
reg81_82_value = adjust_decimals(reg81_82_value)
total_travel_time = xml.SubElement(root, 'total_travel_time')
total_travel_time.text = reg81_82_value
print('Total travel time: ', reg81_82_value, 'μs')

# reg 83-84 real4
reg83_84 = convert_decs_to_bins(data_list_striped[83], data_list_striped[84])
reg83_84_value = struct.unpack("f", struct.pack("L", int(reg83_84,2)))[0]
reg83_84_value = adjust_decimals(reg83_84_value)
delta_travel_time = xml.SubElement(root, 'delta_travel_time')
delta_travel_time.text = reg83_84_value
print('Delta travel time: ', reg83_84_value, 'ns')

# reg 85-86 real4
reg85_86 = convert_decs_to_bins(data_list_striped[85], data_list_striped[86])
reg85_86_value = struct.unpack("f", struct.pack("L", int(reg85_86,2)))[0]
reg85_86_value = adjust_decimals(reg85_86_value)
upstream_travel_time = xml.SubElement(root, 'upstream_travel_time')
upstream_travel_time.text = reg85_86_value
print('Upstream travel time: ', reg85_86_value, 'μs')

# reg 87-88 real4
reg87_88 = convert_decs_to_bins(data_list_striped[87], data_list_striped[88])
reg87_88_value = struct.unpack("f", struct.pack("L", int(reg87_88,2)))[0]
reg87_88_value = adjust_decimals(reg87_88_value)
downstream_travel_time = xml.SubElement(root, 'downstream_travel_time')
downstream_travel_time.text = reg87_88_value
print('Downstream travel time: ', reg87_88_value, 'μs')

# reg 89-90 real4
reg89_90 = convert_decs_to_bins(data_list_striped[89], data_list_striped[90])
reg89_90_value = struct.unpack("f", struct.pack("L", int(reg89_90,2)))[0]
reg89_90_value = adjust_decimals(reg89_90_value)
output_current = xml.SubElement(root, 'output_current')
output_current.text = reg89_90_value
print('Output current: ', reg89_90_value, 'mA')

# reg 92 type INTEGER
reg92 = data_list_striped[92]
reg92_binary = twosCom_decBin(int(reg92), 16)
reg92_value = reg92_binary[-8:]
signal_quality = xml.SubElement(root, 'signal_quality')
signal_quality.text = str(int(reg92_value,2))
print('Signal quality: ', int(reg92_value,2))

# Exporting the xml file with all the sensor values
tree = xml.ElementTree(root)
tree.write("data.xml", xml_declaration=True, encoding='utf-8')


# Binary to float
# https://www.technical-recipes.com/2012/converting-between-binary-and-decimal-representations-of-ieee-754-floating-point-numbers-in-c/

# Binary to decimal converter
# https://www.rapidtables.com/convert/number/binary-to-decimal.html




# ----- User Interface -----
window = Tk()
window.title('Data from TUF-2000M')
window.geometry('900x450')
frame = Frame(window) 

# Labels
fr = Label(window, text = 'Flow Rate').grid(row = 0, column = 0, sticky = E, padx = 5)
efr =    Label(window, text = 'Energy Flow Rate')                .grid(row = 1, column = 0, sticky = E, padx = 5)
v =      Label(window, text = 'Velocity')                        .grid(row = 2, column = 0, sticky = E, padx = 5)
fss =    Label(window, text = 'Fluid sound speed')               .grid(row = 3, column = 0, sticky = E, padx = 5)
pa =     Label(window, text = 'Positive accumulator')            .grid(row = 4, column = 0, sticky = E, padx = 5)
pdf =    Label(window, text = 'Positive decimal fraction')       .grid(row = 5, column = 0, sticky = E, padx = 5)
na =     Label(window, text = 'Negative accumulator')            .grid(row = 6, column = 0, sticky = E, padx = 5)
ndf =    Label(window, text = 'Negative decimal fraction')       .grid(row = 7, column = 0, sticky = E, padx = 5)
pea =    Label(window, text = 'Positive energy accumulator')     .grid(row = 8, column = 0, sticky = E, padx = 5)
pedf =   Label(window, text = 'Positive energy decimal fraction').grid(row = 9, column = 0, sticky = E, padx = 5)
nea =    Label(window, text = 'Negative energy accumulator')     .grid(row = 10, column = 0, sticky = E, padx = 5)
nedf =   Label(window, text = 'Negative energy decimal fraction').grid(row = 11, column = 0, sticky = E, padx = 5)
neta =   Label(window, text = 'Net accumulator')                 .grid(row = 12, column = 0, sticky = E, padx = 5)
netdf =  Label(window, text = 'Net decimal fraction')            .grid(row = 13, column = 0, sticky = E, padx = 5)
netea =  Label(window, text = 'Net energy accumulator')          .grid(row = 14, column = 0, sticky = E, padx = 5)
netedf = Label(window, text = 'Net energy decimal fraction')     .grid(row = 15, column = 0, sticky = E, padx = 5)
t1 =     Label(window, text = 'Temperature #1/inlet')            .grid(row = 16, column = 0, sticky = E, padx = 5)
t2 =     Label(window, text = 'Temperature #2/outlet')           .grid(row = 17, column = 0, sticky = E, padx = 5)
ai3 =    Label(window, text = 'Analog input AI3')                .grid(row = 18, column = 0, sticky = E, padx = 5)
ai4 =    Label(window, text = 'Analog input AI4')                .grid(row = 19, column = 0, sticky = E, padx = 5)
ai5 =    Label(window, text = 'Analog input AI5')                .grid(row = 20, column = 0, sticky = E, padx = 5)
ci3a =   Label(window, text = 'Current input AI3')               .grid(row = 0, column = 3, sticky = E, padx = 5)
ci3b =   Label(window, text = 'Current input AI3')               .grid(row = 1, column = 3, sticky = E, padx = 5)
ci3c =   Label(window, text = 'Current input AI3')               .grid(row = 2, column = 3, sticky = E, padx = 5)
r49 =    Label(window, text = 'System password')                 .grid(row = 3, column = 3, sticky = E, padx = 5)
r51 =    Label(window, text = 'Password for hardware')           .grid(row = 4, column = 3, sticky = E, padx = 5)
d =      Label(window, text = 'Date')                            .grid(row = 5, column = 3, sticky = E, padx = 5)
r56 =    Label(window, text = 'Day + Hour for Autosave')         .grid(row = 6, column = 3, sticky = E, padx = 5)
kti =    Label(window, text = 'Key to input')                    .grid(row = 7, column = 3, sticky = E, padx = 5)
gtw =    Label(window, text = 'Go to Window #')                  .grid(row = 8, column = 3, sticky = E, padx = 5)
lcd =    Label(window, text = 'LCD Back-lit lights for number of seconds').grid(row = 9, column = 3, sticky = E, padx = 5)
tftb =   Label(window, text = 'Times for the beeper')            .grid(row = 10, column = 3, sticky = E, padx = 5)
plfo =   Label(window, text = 'Pulses left for OCT')             .grid(row = 11, column = 3, sticky = E, padx = 5)
ec =     Label(window, text = 'Error code')                      .grid(row = 12, column = 3, sticky = E, padx = 5)
roi =    Label(window, text = 'PT100 resistance of inlet')       .grid(row = 13, column = 3, sticky = E, padx = 5)
rou =    Label(window, text = 'PT100 resistance of outlet')      .grid(row = 14, column = 3, sticky = E, padx = 5)
ttt =    Label(window, text = 'Total travel time')               .grid(row = 15, column = 3, sticky = E, padx = 5)
dtt =    Label(window, text = 'Delta travel time')               .grid(row = 16, column = 3, sticky = E, padx = 5)
utt =    Label(window, text = 'Upstream travel time')            .grid(row = 17, column = 3, sticky = E, padx = 5)
downtt = Label(window, text = 'Downstream travel time')          .grid(row = 18, column = 3, sticky = E, padx = 5)
oc =     Label(window, text = 'Output current')                  .grid(row = 19, column = 3, sticky = E, padx = 5)
sq =     Label(window, text = 'Signal quality')                  .grid(row = 20, column = 3, sticky = E, padx = 5)

# Values
frv =     Label(window, text = reg1_2_value)  .grid(row = 0, column = 1, sticky = W, padx = 5)
efrv =    Label(window, text = reg3_4_value)  .grid(row = 1, column = 1, sticky = W, padx = 5)
vv =      Label(window, text = reg5_6_value)  .grid(row = 2, column = 1, sticky = W, padx = 5)
fssv =    Label(window, text = reg7_8_value)  .grid(row = 3, column = 1, sticky = W, padx = 5)
pav =     Label(window, text = reg9_10_value) .grid(row = 4, column = 1, sticky = W, padx = 5)
pdfv =    Label(window, text = reg11_12_value).grid(row = 5, column = 1, sticky = W, padx = 5)
nav =     Label(window, text = reg13_14_value).grid(row = 6, column = 1, sticky = W, padx = 5)
ndfv =    Label(window, text = reg15_16_value).grid(row = 7, column = 1, sticky = W, padx = 5)
peav =    Label(window, text = reg17_18_value).grid(row = 8, column = 1, sticky = W, padx = 5)
pedfv =   Label(window, text = reg19_20_value).grid(row = 9, column = 1, sticky = W, padx = 5)
neav =    Label(window, text = reg21_22_value).grid(row = 10, column = 1, sticky = W, padx = 5)
nedfv =   Label(window, text = reg23_24_value).grid(row = 11, column = 1, sticky = W, padx = 5)
netav =   Label(window, text = reg25_26_value).grid(row = 12, column = 1, sticky = W, padx = 5)
netdfv =  Label(window, text = reg27_28_value).grid(row = 13, column = 1, sticky = W, padx = 5)
neteav =  Label(window, text = reg29_30_value).grid(row = 14, column = 1, sticky = W, padx = 5)
netedfv = Label(window, text = reg31_32_value).grid(row = 15, column = 1, sticky = W, padx = 5)
t1v =     Label(window, text = reg33_34_value).grid(row = 16, column = 1, sticky = W, padx = 5)
t2v =     Label(window, text = reg35_36_value).grid(row = 17, column = 1, sticky = W, padx = 5)
ai3v =    Label(window, text = reg37_38_value).grid(row = 18, column = 1, sticky = W, padx = 5)
ai4v =    Label(window, text = reg39_40_value).grid(row = 19, column = 1, sticky = W, padx = 5)
ai5v =    Label(window, text = reg41_42_value).grid(row = 20, column = 1, sticky = W, padx = 5)
ci3av =   Label(window, text = reg43_44_value).grid(row = 0, column = 4, sticky = W, padx = 5)
ci3bv =   Label(window, text = reg45_46_value).grid(row = 1, column = 4, sticky = W, padx = 5)
ci3cv =   Label(window, text = reg47_48_value).grid(row = 2, column = 4, sticky = W, padx = 5)
r49 =     Label(window, text = reg49_50)      .grid(row = 3, column = 4, sticky = W, padx = 5)
r51 =     Label(window, text = reg51)         .grid(row = 4, column = 4, sticky = W, padx = 5)
dv =      Label(window, text = date)          .grid(row = 5, column = 4, sticky = W, padx = 5)
r56 =     Label(window, text = reg56)         .grid(row = 6, column = 4, sticky = W, padx = 5)
ktiv =    Label(window, text = reg59)         .grid(row = 7, column = 4, sticky = W, padx = 5)
gtwv =    Label(window, text = reg60)         .grid(row = 8, column = 4, sticky = W, padx = 5)
lcdv =    Label(window, text = reg61)         .grid(row = 9, column = 4, sticky = W, padx = 5)
tftbv =   Label(window, text = reg62)         .grid(row = 10, column = 4, sticky = W, padx = 5)
plfov =   Label(window, text = reg62)         .grid(row = 11, column = 4, sticky = W, padx = 5)
ecv =     Label(window, text = reg72)         .grid(row = 12, column = 4, sticky = W, padx = 5)
roiv =    Label(window, text = reg77_78_value).grid(row = 13, column = 4, sticky = W, padx = 5)
rouv =    Label(window, text = reg79_80_value).grid(row = 14, column = 4, sticky = W, padx = 5)
tttv =    Label(window, text = reg81_82_value).grid(row = 15, column = 4, sticky = W, padx = 5)
dttv =    Label(window, text = reg83_84_value).grid(row = 16, column = 4, sticky = W, padx = 5)
uttv =    Label(window, text = reg85_86_value).grid(row = 17, column = 4, sticky = W, padx = 5)
downttv = Label(window, text = reg87_88_value).grid(row = 18, column = 4, sticky = W, padx = 5)
ocv =     Label(window, text = reg89_90_value).grid(row = 19, column = 4, sticky = W, padx = 5)
sqv =     Label(window, text = int(reg92_value,2)).grid(row = 20, column = 4, sticky = W, padx = 5)

# Units
fru =     Label(window, text = u'm\u00B3/h').grid(row = 0, column = 2, sticky = W, padx = 5)
efru =    Label(window, text = 'GJ/h')      .grid(row = 1, column = 2, sticky = W, padx = 5)
vu =      Label(window, text = 'm/s')       .grid(row = 2, column = 2, sticky = W, padx = 5)
fssu =    Label(window, text = 'm/s')       .grid(row = 3, column = 2, sticky = W, padx = 5)
t1u =     Label(window, text = u'\u00B0C')  .grid(row = 16, column = 2, sticky = W, padx = 5)
t2u =     Label(window, text = u'\u00B0C')  .grid(row = 17, column = 2, sticky = W, padx = 5)
ci3au =   Label(window, text = 'mA')        .grid(row = 0, column = 5, sticky = W, padx = 5)
ci3bu =   Label(window, text = 'mA')        .grid(row = 1, column = 5, sticky = W, padx = 5)
ci3cu =   Label(window, text = 'mA')        .grid(row = 2, column = 5, sticky = W, padx = 5)
lcdu =    Label(window, text = 'sec')       .grid(row = 9, column = 5, sticky = W, padx = 5)
roiu =    Label(window, text = 'Ohm')       .grid(row = 13, column = 5, sticky = W, padx = 5)
rouu =    Label(window, text = 'Ohm')       .grid(row = 14, column = 5, sticky = W, padx = 5)
tttu =    Label(window, text = 'μs')        .grid(row = 15, column = 5, sticky = W, padx = 5)
dttu =    Label(window, text = 'ns')        .grid(row = 16, column = 5, sticky = W, padx = 5)
uttu =    Label(window, text = 'μs')        .grid(row = 17, column = 5, sticky = W, padx = 5)
downttu = Label(window, text = 'μs')        .grid(row = 18, column = 5, sticky = W, padx = 5)
ocv =     Label(window, text = 'mA')        .grid(row = 19, column = 5, sticky = W, padx = 5)

window.mainloop()
