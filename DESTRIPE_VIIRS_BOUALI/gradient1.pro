;+
; NAME:
;       gradient1
;
; PURPOSE:
;       Computes the gradient of an image using 
;       forward finite differences and Neumann boundary conditions
;       
; CALLING SEQUENCE:
;      dfdx = gradient1(image, opt)
;      
; INPUTS:
;   img:   imput image 
;   opt  : Option to be specified for vertical or horizontal component of the gradient field
;                                 
; OUPUTS:
;    opt = 1, output is gx, the horizontal gradient of the image
;    opt = 2, output is gy, the vertical gradient of the image
;    
; HISTORY:
;   2011-12-04 - Marouan Bouali


Function gradient1, img, opt

; Get the size of the image
s = size(img)
; Number of lines 
sx = s(2)
; Number of columns
sy = s(1) 

img = float(img)

; Compute the horizontal gradient
if opt eq 1 then begin
gx = fltarr(sy,sx)
gx(0:sy-2,*) = img(1:sy-1,*)-img(0:sy-2,*)
gx(sy-1,*) = 0
return, gx
endif

; Compute the vertical gradient
if opt eq 2 then begin
gy = fltarr(sy,sx)
gy(*,0:sx-2) = img(*,1:sx-1)-img(*,0:sx-2)
gy(*,sx-1) = 0
return, gy
endif

END