import torch
import torch.nn.functional as F
import bmtrain as bmt

class Linear(bmt.DistributedModule):
    def __init__(self, in_features : int, out_features: int, bias: bool = True, dtype = None) -> None:
        super().__init__()

        self.in_features = in_features
        self.out_features = out_features
        self.weight = bmt.DistributedParameter(torch.empty(out_features, in_features, dtype=dtype, device="cuda"), init_method=torch.nn.init.xavier_normal_)
        if bias:
            self.bias = bmt.DistributedParameter(torch.empty(out_features, dtype=dtype, device="cuda"), init_method=torch.nn.init.zeros_)
        else:
            self.register_parameter('bias', None)
    
    def forward(self, input):
        return F.linear(input, self.weight, self.bias)

    def extra_repr(self) -> str:
        return f'in_features={self.in_features}, out_features={self.out_features}, bias={self.bias is not None}'