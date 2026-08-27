#field_of_view
"""
challenge->user input's the FOV & coords. from telescope
the function will calculate with the provided data
if the sat trains could block their view
-> generate alerts or warn the users on the Observatory site
"""


def field_of_view_coord():

    x = input("enter x coordinate: ")
    y = input("enter y coordinate: ")
    coord = [float(x), float(y)]
    if coord != [float(x), float(y)]:
        raise ValueError()
    else:
        return coord

coord = field_of_view_coord()
print(coord)



def FOV_lenght():
    fov = input("enter the FOV sensor: ")
    fov = float(fov)
    return fov
fov = FOV_lenght()
print(fov)



"""
first we pass the observer data
and make the comparison between
TLE data transformed to AR-DEC
"""