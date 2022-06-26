from expects import expect, equal
from mamba import description, it

with description('Canary Spec') as self:
    with it('environment is properly configured'):
        expect(True).to(equal(True))
