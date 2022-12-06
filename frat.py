import numpy as np

class frt(object):
    
    def __init__(self, folded=False):
        self.folded = folded
        self.n_vecs = None
        
    def _cp(self, x, p):
        return x - p*np.round(x / p)
        
    def compute_nvecs(self, p):
        n_vecs = [[0.0, 1.0]]
        for k in range(1, p):
            u_k = np.array((-k, 1))
            n_vecs_cand = []
            dists = []
            for n in range(1, p):
                ak_bk = [self._cp(x, p) for x in np.mod(n*u_k, p)]
                if ak_bk[1] < 0:
                    continue
                n_vecs_cand.append(ak_bk)
                dists.append(np.linalg.norm(ak_bk, ord=np.inf))
            best_vec = n_vecs_cand[np.argmin(dists)]
            if self.folded:
                if best_vec[0] >= 0:
                    n_vecs.append(best_vec)
            else:
                n_vecs.append(best_vec)
        n_vecs.append([1.0, 0.0])
        return n_vecs
    
    def fit(self, img):
        if self.folded:
            self.n = img.shape[0]
            self.p = 2*self.n - 1
        else:
            self.n = self.p = img.shape[0]
        self.n_vecs = self.compute_nvecs(self.p)
        return None
        
    def transform(self, img):
        if len(img.shape) != 2:
            raise ValueError('Must be 2D data')
        if img.shape[0] != img.shape[1]:
            raise ValueError('Input image must be square')
        if img.shape[0] != self.n:
            raise ValueError(f'Input image must be {self.n} x {self.n}')
        
        if self.folded:
            img_folded = np.empty((self.p, self.p))
            img_folded[:self.n, self.n-1:] = img
            img_folded[:self.n, :self.n] = img[:, ::-1]
            img_folded[self.n-1:, self.n-1:] = img[::-1, :]
            img_folded[self.n-1:, :self.n] = img[::-1, ::-1]
            self._img = img_folded - img_folded.mean()
        else:
            self._img = img.copy() - img.mean()

        self.r = np.zeros((self._img.shape[0], len(self.n_vecs)))
        for col, n_vec in enumerate(self.n_vecs):
            for i in range(self.p):
                if n_vec[1] == 0:
                    self.r[:, col] = np.sum(self._img, axis=0)
                else:
                    x_step = n_vec[1]
                    y_step = -n_vec[0]
                    self.r[:, col] += np.roll(self._img[:, int(i * x_step) % self.p], int(i * y_step) % self.p)

        return 1/np.sqrt(self.p) * self.r
        
    def fit_transform(self, img):
        if self.n_vecs is None:
            self.fit(img)
        return self.transform(img)
    
    def inv_transform(self, sino):
        if self.n_vecs is None:
            raise ValueError('Need to first fit to image size')
        
        if not self.folded:
            self.recon = np.zeros((self.n, self.n), dtype=np.float64)
            for col, n_vec in enumerate(self.n_vecs):
                for i in range(self.n):
                    if n_vec[1] == 0:
                        self.recon[i, :] += sino[:, col]
                    else:
                        x_step = -n_vec[1]
                        y_step = n_vec[0]
                        self.recon[:, int(i * x_step) % self.p] += np.roll(sino[:, col], int(-i * y_step) % self.p)
        else:
            self.recon = np.zeros((self.p, self.p), dtype=np.float64)
            for col, n_vec in enumerate(self.n_vecs):
                for i in range(self.p):
                    if n_vec[1] == 0:
                        self.recon[i, :] += sino[:, col]
                    else:
                        x_step = n_vec[1]
                        y_step = -n_vec[0]
                        if n_vec[0] == 0:
                            self.recon[:, int(i * x_step) % self.p] += np.roll(sino[:, col], int(-i * y_step) % self.p)
                        else:
                            self.recon[:, int(i * x_step) % self.p] += np.roll(sino[:, col], int(-i * y_step) % self.p)
                            self.recon[:, int(i * x_step - 1) % self.p] += np.roll(sino[:, col], int(i * y_step) % self.p)
            self.recon = self.recon[:self.n, :self.n][:, ::-1]
        
        return 1/np.sqrt(self.p) * self.recon