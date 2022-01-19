DefineConstant[ domain_size = 1.0 ];
DefineConstant[ mesh_size = domain_size/4.0 ];

SetFactory("OpenCASCADE");
Rectangle(1) = {0, 0, 0, domain_size, domain_size, 0};
Physical Surface(1) = {1};
