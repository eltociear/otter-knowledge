import torch


class TransE(torch.nn.Module):
    """A class implementing the TransE scoring function as a PyTorch module"""

    def __init__(self, n_rel, n_dim, p_norm=2, normalize=True, device='cpu'):
        super(TransE, self).__init__()
        self.device = device
        self.n_rel = n_rel
        self.n_dim = n_dim
        self.p_norm = p_norm
        self.normalize = normalize

        self.R = torch.nn.Parameter(
            torch.rand(n_rel, n_dim))  # random initialise trainable weights for scoring function
        self.to(self.device)

    def forward(self, embeddings, triples):
        s, r, o = embeddings[triples[0, :], :], self.R[triples[1, :], :], embeddings[triples[2, :], :]

        if self.normalize:
            s = F.normalize(s, p=self.p_norm, dim=-1)
            o = F.normalize(o, p=self.p_norm, dim=-1)

        return -(s + r - o).norm(p=self.p_norm, dim=-1)

    def extend(self, n_rel):
        r = TransE(n_rel, self.n_dim, self.p_norm, self.normalize)
        state_dict = r.state_dict()
        old_parameters = self.state_dict()['R'].detach() + 0.0
        state_dict['R'] = torch.cat([old_parameters, torch.randn(n_rel - self.n_rel, self.n_dim).to(self.device)])
        r.load_state_dict(state_dict)
        return r
