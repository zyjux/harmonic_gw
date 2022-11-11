pro run_ds

print,'Read gif image...'
read_gif,'stripes.gif',image,r,g,b

; Crop off the footer
image_crop = image(*,12:719)
sz = size(image_crop,/dimension)

print,'Plotting original imagery'
window,0,retain=2,xs=sz(0),ys=sz(1),tit='ORIGINAL CROPPED'
tv,image_crop
write_jpeg,'Original.jpg',image_crop

a = fltarr(sz(1))
b = fltarr(sz(1))
for i=0,sz(1)-1 do begin
 a(i) = mean(image_crop(*,i))
 b(i) = stdev(image_crop(*,i))
endfor ;i

all_mean = mean(a)
all_stdev = mean(b)

image_crop_new = image_crop
num_fix = 0
mean_frac = 0.4
std_frac = 0.4
for i=0,sz(1)-1 do begin
 if ((a(i) lt mean_frac*all_mean or a(i) gt (1.0+mean_frac)*all_mean) or (b(i) lt std_frac*all_stdev)) then begin
  image_crop_new(*,i) = fix((image_crop(*,i-1)*1.0+image_crop(*,i+1)*1.0)/2.)
  num_fix = num_fix+1
  print,'Fixed index: i = ',i
 endif
endfor ;i
print,'Total number of lines fixed = ',num_fix

print,'Plotting line-drop-out corrected original imagery'
window,1,retain=2,xs=sz(0),ys=sz(1),tit='ORIGINAL LINECORR'
tv,image_crop_new
write_jpeg,'Original_DropOut.jpg',image_crop_new

; Call destripe code
; typical: theta = 0.1, eps = 1
print,'Calling destriper code...'
theta = 0.3
theta_str = '0.3'
n_iteration = 120 
iter_str = '120'
eps = 1
eps_str = '1'

image_destripe = fix(destripe_uvdm(image_crop_new*1.0,theta,n_iteration,eps))

print,'Plotting imagery after destripe'

window,2,retain=2,xs=sz(0),ys=sz(1),tit='DESTRIPED LINECORR'
tv,image_destripe
write_jpeg,'Destripe_THETA_'+theta_str+'_EPS_'+eps_str+'_ITER_'+iter_str+'.jpg',image_destripe

mean_row = fltarr(sz(1))
for i=0,sz(1)-1 do begin
 mean_row(i) = mean(image_destripe(*,i)*1.0)
endfor ;i
all_mean = mean(mean_row)

boxcar_size = 6
bias_factor = smooth((mean_row/all_mean),boxcar_size,/edge_truncate)

image_destripe_biascorr = fltarr(sz(0),sz(1))
for i=0,sz(1)-1 do begin
 image_destripe_biascorr(*,i) = fix(image_destripe(*,i)*1.0/bias_factor(i))
endfor ;i

high_indices = where(image_destripe_biascorr gt 255,count_high)
if (count_high gt 0) then image_destripe_biascorr(high_indices) = 255

window,3,retain=2,xs=sz(0),ys=sz(1),tit='DESTRIPED LINECORR BIASCORR'
tv,image_destripe_biascorr
write_jpeg,'Destripe_BiasCorr_THETA_'+theta_str+'_EPS_'+eps_str+'_ITER_'+iter_str+'.jpg',image_destripe_biascorr

STOP

exit

end
