#     CS303 Cellular Automata Simulator
#     Copyright (C) 2009 Hampshire College CS303
#     
#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#     
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#     
#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see <http://www.gnu.org/licenses/>.

from BaseCA import BaseCA, TorroidalCA
from Wolfram import Wolfram
from SpectorMachine import SpectorMachine
from Nasch import Nasch

#Hack, probably not perfect but availCAs is only used to check that
#the user has provided a CA class at the command line.
availCAs = [x for x in locals().keys() if not x.startswith("_")]
