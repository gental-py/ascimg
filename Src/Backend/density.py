class DensityScale:
    register = {}

    def __init__(self, scale: str) -> None:
        self.text_scale = scale
        self.range_scale = self.build_scale()
        
    def build_scale(self) -> dict[range, str]:
        step = round(256/len(self.text_scale))+1
        range_scale = {}
        
        scale_index = 0
        for range_index in range(-1, 256, step):
            rng = range(range_index+1, range_index+step+1)
            range_scale[rng] = self.text_scale[scale_index]
            scale_index += 1
    
        return range_scale
    
    def get(self, value: int) -> str:
        """ Return character assigned to given pixel's value. """
        for rng, chr in self.range_scale.items():
            if value in rng:
                return chr
            
    def register_scale(self, name: str) -> None:
        """ Save scale to DensityScale.register """
        DensityScale.register[name] = self
            

DensityScale(" .:-=+*#%@").register_scale("short")
DensityScale("0123456789").register_scale("numeric")
