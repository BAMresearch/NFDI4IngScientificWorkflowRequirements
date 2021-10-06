// Partition of the unit square into NTransfinite - 1 triangles per spatial direction.
Mesh.SecondOrderIncomplete = 0;
NTransfinite = 5;

p0 = newp;
Point(p0) = {0.0, 0.0, 0.0, 0.25};
p1 = newp;
Point(p1) = {1.0, 0.0, 0.0, 0.25};
p2 = newp;
Point(p2) = {1.0, 1.0, 0.0, 0.25};
p3 = newp;
Point(p3) = {0.0, 1.0, 0.0, 0.25};
l0 = newl;
Line(l0) = {p0, p1};
l1 = newl;
Line(l1) = {p1, p2};
l2 = newl;
Line(l2) = {p2, p3};
l3 = newl;
Line(l3) = {p3, p0};
ll0 = newll;
Line Loop(ll0) = {l0, l1, l2, l3};
s0 = news;
Plane Surface(s0) = {ll0};
Transfinite Line {l0, l2} = NTransfinite;
Transfinite Line {l1, l3} = NTransfinite;
Transfinite Surface {s0};
Physical Surface("surface") = {s0};
