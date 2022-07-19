(define-module (sigwftools)
  #:use-module (gnu packages algebra)
  #:use-module (gnu packages base)
  #:use-module (gnu packages compression)
  #:use-module (gnu packages cpp)
  #:use-module (gnu packages fontutils)
  #:use-module (gnu packages gl)
  #:use-module (gnu packages image)
  #:use-module (gnu packages maths)
  #:use-module (gnu packages pdf)
  #:use-module (gnu packages protobuf)
  #:use-module (gnu packages python)
  #:use-module (gnu packages qt)
  #:use-module (gnu packages serialization)
  #:use-module (gnu packages textutils)
  #:use-module (gnu packages xiph)
  #:use-module (gnu packages xml)
  #:use-module (guix download)
  #:use-module (guix packages)
  #:use-module (guix build-system cmake)
  #:use-module ((guix licenses) #:prefix license:)
  )

(define-public my-glibc-utf8-locales
  (make-glibc-utf8-locales
   glibc #:locales (list "en_US") #:name "my-glibc-utf8-locales"))


(define-public cgns
  (package
   (name "cgns")
   (version "4.3.0")
   (source
    (origin
     (method url-fetch)
     (uri "https://github.com/CGNS/CGNS/archive/refs/tags/v4.3.0.tar.gz")
     (sha256
       (base32 "0cm0q2ppflfw6jy3ykk2asaqvvza17qq7wggs46yl7bkk5yyn2bp"))))
   (build-system cmake-build-system)
   (inputs (list hdf5))
   (arguments
    `(#:build-type "Release"
      ; There are no tests.
      #:phases (modify-phases %standard-phases (delete 'check))))
   (home-page "https://cgns.org/")
   (synopsis "The CFD General Notation System (CGNS) provides a general, portable, and extensible standard for the storage and retrieval of computational fluid dynamics (CFD) analysis data.")
   (description "The system consists of two parts: (1) a standard format for recording the data, and (2) software that reads, writes, and modifies data in that format.  The format is a conceptual entity established by the documentation; the software is a physical product supplied to enable developers to access and produce data recorded in that format.")
   (license license:zlib)))


(define-public paraview
  (package
   (name "paraview")
   (version "5.9.1")
   (source
    (origin
     (method url-fetch)
     (uri "https://www.paraview.org/files/v5.9/ParaView-v5.9.1.tar.xz")
     (sha256
       (base32 "13aczmfshzia324h9r2m675yyrklz2308rf98n444ppmzfv6qj0d"))))
   (build-system cmake-build-system)
   (propagated-inputs
    (list mesa qtbase-5 qtsvg-5 glew))
   (inputs
    (list python qtxmlpatterns utfcpp pugixml qttools-5 double-conversion lz4
     eigen cli11 netcdf gl2ps zlib libjpeg-turbo libpng libtiff expat freetype
     jsoncpp libharu libxml2 hdf5 libtheora protobuf cgns))
   (arguments
    `(#:phases
      (modify-phases
       %standard-phases
       (add-after
        'unpack 'patch-haru
        (lambda* (#:key inputs #:allow-other-keys)
                 (substitute* "VTK/ThirdParty/libharu/CMakeLists.txt"
                              (("2.4.0") "2.3.0"))
                 #t)))
      #:build-type "Release" ; Build without '-g' to save space.
      #:configure-flags
      (list
       "-DPARAVIEW_USE_PYTHON=ON"
       "-DPARAVIEW_BUILD_WITH_EXTERNAL=ON"
       "-DPARAVIEW_ENABLE_WEB:BOOL=OFF"
       "-DVTK_MODULE_USE_EXTERNAL_ParaView_vtkcatalyst=OFF"
       "-DVTK_MODULE_USE_EXTERNAL_VTK_cgns=OFF"
       "-DVTK_MODULE_USE_EXTERNAL_VTK_exprtk=OFF"
       "-DVTK_MODULE_USE_EXTERNAL_VTK_fmt=OFF"
       "-DVTK_MODULE_USE_EXTERNAL_VTK_ioss=OFF")))
   (home-page "https://www.paraview.org/")
   (synopsis "ParaView is an open-source, multi-platform data analysis and visualization application")
   (description "ParaView users can quickly build visualizations to analyze their data using qualitative and quantitative techniques. The data exploration can be done interactively in 3D or programmatically using ParaView’s batch processing capabilities.")
   (license license:bsd-3)))
