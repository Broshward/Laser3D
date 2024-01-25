difference(){
    cube([21,32,1],true);
    translate([0,0.3,-5]) linear_extrude(10) import("Laser_int.pcb.svg");
}
    translate([21,0.3,0]) linear_extrude(10) import("Laser_int.pcb.svg");
