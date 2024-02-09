difference(){
    cube([21,32,1]);
    translate([0,0,-0.1]) cooper();
}
//cooper();
module cooper(){
    difference(){
        linear_extrude(1.5) import("Laser_int.pcb.svg");
        translate([0,0,-0.1]) linear_extrude(2) import("Laser_int.pcb_drill.svg");
    }
}   
