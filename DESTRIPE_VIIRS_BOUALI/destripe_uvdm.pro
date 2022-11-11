;+
; NAME:
;       Destripe_UVDM
;
; PURPOSE:
;       Destriping based on a unidirectional variational model (Bouali and Ladjal, 2011, IEEE TGRS,
;        " Towards Optimal Destriping of MODIS Data using a Unidirectional Variational Model")
;        
;        Note: This implementation is based on a Guauss-Seidel iterative scheme
;              
; CALLING SEQUENCE:
;      image_out = Destripe_UVDM(image, theta, n_iteration, eps)
;      
; INPUTS:
;   img: input image
;   n_iteration: number of iterations in the Gauss-Seidel scheme
;   eps: epsilon value for the non differientabiliy of UVDM at 0 (similiar eps for vertical and horizontal directions)
;   theta: Lagrangian multiplier to adjust degree of regularization
;                                   
; OUPUTS:
;   image_out: destriped image 
;    
; HISTORY:
;   2011-12-04 - Marouan Bouali
;   2013-03-28 - Steve Miller (very minor edits to automate the convergence check)


;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;                                 Note on parameter selection
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;                            
; For 8 bits images, typical values are theta = 0.1 and eps = 1 
; The selection of theta, eps and iteration number should ensure that:
;  - Image Distortion is higher than 95%
;  - No blur artifacts appear near sharp edges (this occurs if eps is too large)
;  - The solution is close enough to the minimizer of the energy functional  (check for convergence)
; 

Function Destripe_UVDM, img, theta, n_iteration, eps

s = size(img)
; Number of lines
sy = s(2) 
; Number of columns
sx = s(1)

; Initialize the energy functional
energy_function = fltarr(n_iteration)

; Initialize Image Distortion (ID)
ID = fltarr(n_iteration)

; Initialize Radiometric Improvement Factor (RIF)
RIF = fltarr(n_iteration)

; Initialize window size to monitor destriping
; Steve comment out for now
; For each iteration, the window will display: original image + destriped image + extracted stripe noise
;WINDOW, 3, XSIZE = 3*s[1], YSIZE = 1*s[2]

; Initialize estimate of solution
u_0 = float(img)

; Compute gradient field of noisy image 
gx = gradient1(img,1)
gy = gradient1(img,2)

; Start Gauss-Seidel 
for i=0L, n_iteration-1 do begin

; Compute gradient field of solution for convergence analysis
tx = gradient1(u_0,1)
ty = gradient1(u_0,2)

u_f = u_0-img

; Calculate denominator variables

ce = 1/(sqrt(([u_f(1:sx-1,*),(u_f(sx-1,*))]-u_f )^2 + eps))
cw = 1/(sqrt((u_f-[(u_f(0,*)),u_f(0:sx-2,*)] )^2 + eps))
cs = 1/(sqrt(([[u_0(*,1:sy-1)],[u_0(*,sy-1)]]-u_0)^2 + eps))
cn = 1/(sqrt((u_0-[[u_0(*,0)],[u_0(*,0:sy-2)]])^2 + eps))

term1 = ce*([u_0(1:sx-1,*),u_0(sx-1,*)] - [img(1:sx-1,*),img(sx-1,*)] + img)
term2 = cw*([u_0(0,*),u_0(0:sx-2,*)] -  [img(0,*),img(0:sx-2,*)] + img  )
term3 = theta*cs*([[u_0(*,1:sy-1)],[u_0(*,sy-1)]])
term4 = theta*cn*([[u_0(*,0)],[u_0(*,0:sy-2)]])

denominator = ce+cw+theta*cs+theta*cn

; Update solution
u_0 = (term1+term2+term3+term4)/denominator

; Compute Image Distortion for current solution
ID(i)=100 - (total(abs(gx(*)-tx(*))))*100/total(abs(gx(*)))

; Compute Radiometric Improvement Factor for current solution
RIF(i)=(total(abs(gy(*)))-total(abs(ty(*))))*100/total(abs(gy(*)))

; Compute energy functional for current solution
energy_function(i)=total(sqrt((tx(*)-gx(*))^2+eps))+theta*total(sqrt((ty(*))^2+eps))

if i gt 0 then begin
 print, 'Iteration ' + strtrim(string(i),1) + '      ' + ' Image Distortion = ' + strtrim(string(ID(i)),1)+ '      ' + ' Improvement Factor = ' + strtrim(string(RIF(i)),1)
endif

; Scales data for direct graphics display and outputs data to image display at the specified location.  Array is scaled so the minimum
; data value becomes 0 and the maximum value becomes the maximum number of available colors (!d.table_size)
; This will update at each successive iteration of the i-loop

; Steve Comment out for now
;TVscl, rebin(((img)),s[1],s[2]),0
;TVscl, rebin(((u_0)),s[1],s[2]),1
;TVscl, rebin((img-u_0),s[1],s[2]),2

; Test for convergence in energy function here, and bail out if converged
; Steve Comment out for now
;energy_func_convthresh = ???
;if ((i gt 0) and ((energy_function(i)-energy_function(i-1)) lt energy_func_convthresh)) then begin
; print,'Convergence in energy function achieved, bailing out now'
; goto,bail_out
;endif

endfor ;i loop

; Jump to here early if energy function convergence criteria are met
bail_out:

; Plot energy functional to check for convergence
; Steve Comment out for now
;iplot, energy_function

return, u_0

END

