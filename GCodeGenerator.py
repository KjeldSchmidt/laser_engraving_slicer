from typing import Dict


def initialize_printer( x_init: float, y_init: float, z_init: float ) -> str:
	initial_position_line = f'G1 X{x_init:.2f} Y{y_init:.2f} Z{z_init:.2f} ; Move laser to lower left corner of printing bed'

	initial_lines = [
		'G90 ; Set coordinate system to absolute values in X, Y, Z',
		'M106 S0 ; Turn off the laser',
		'G28 ; Home all axes. Depending on the material to print on, homing Z may be undesirable/bad',
		initial_position_line,
		'G92 X0 Y0 ; Reset Coordinate System',
	]

	return '\n'.join( initial_lines )


def make_gcode( settings: Dict ) -> str:
	print( settings )
	start = initialize_printer( settings[ 'x_init' ], settings[ 'y_init' ], settings[ 'z_init' ] )
	return start
