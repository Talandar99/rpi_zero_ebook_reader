$fn = 100;
screen_height = 2137;

module raspberry() {
  tolerancy = 0.5;
  raspberry_x = 30 + tolerancy;
  raspberry_y = 65 + tolerancy;
  shield_height = 26;
  screw_hole_radius = 1.5;

  translate(v=[1, 1, 2]) difference() {
      union() {

        translate(v=[-1, -1, -2]) cube(size=[1, raspberry_y * 0.60 + 2, 15], center=false);
        translate(v=[-1, -1, -2]) cube(size=[raspberry_x + 2, raspberry_y + 2, 7], center=false);
        translate(v=[raspberry_x, -1, -2]) cube(size=[1, raspberry_y + 2, shield_height], center=false);
        translate(v=[raspberry_x / 3 + raspberry_x / 3, raspberry_y, -2]) cube(size=[raspberry_x / 3, 1, shield_height], center=false);
        translate(v=[raspberry_x / 3 + raspberry_x / 3, -1, -2]) cube(size=[raspberry_x / 3, 1, shield_height], center=false);
      }
      {
        cube(size=[raspberry_x, raspberry_y, screen_height], center=false);
        translate(v=[3.5, 3.5, -5]) cylinder(h=10, r=screw_hole_radius, center=false);
        translate(v=[3.5, raspberry_y - 3.5, -5]) cylinder(h=10, r=screw_hole_radius, center=false);
        translate(v=[raspberry_x - 3.5, 3.5, -5]) cylinder(h=10, r=screw_hole_radius, center=false);
        translate(v=[raspberry_x - 3.5, raspberry_y - 3.5, -5]) cylinder(h=10, r=screw_hole_radius, center=false);
      }
    }
}
module screen() {
  color(c="gray", alpha=1.0) {
    cube(size=[112, 172, screen_height], center=false);
    translate(v=[0, 77, 0]) {
      cube(size=[133, 15, screen_height], center=false);
      translate(v=[132, -9, 0]) cube(size=[18, 32, screen_height], center=false);
    }
    translate(v=[120, 0, 0]) {
      raspberry();
    }
  }
}
module button() {
  translate(v=[5.2, 5.2, -5]) cube(size=[1, 1, 10], center=false);
  translate(v=[0, 5.2, -5]) cube(size=[1, 1, 10], center=false);
  translate(v=[5.2, 0, -5]) cube(size=[1, 1, 10], center=false);
  translate(v=[0, 0, -5]) cube(size=[1, 1, 10], center=false);
  cube(size=[6.20, 6.20, 10], center=false);
}

raspberry();
