from pprint import pprint

from expects import expect, equal, have_len
from mamba import description, it, before

from spec.test_parsing_spike_test import parse_ast_of, MyVisitor, DuplicatedLines

with description('Repeated lines finder') as self:
    with description('in sample 1'):
        with before.each:
            self.ast = parse_ast_of('sample_declarations_1.c')
            self.generator = MyVisitor(DuplicatedLines())

        with it('finds repeated lines in the sample 1'):
            self.generator.visit(self.ast)
            repeated_lines_list = self.generator.duplicated_lines.list
            print("")
            pprint(repeated_lines_list)
            variable_names = [x['variable']['name'] for x in repeated_lines_list]
            expect(variable_names).to(equal(['key__repeated', 'counter__repeated']))
            expect(repeated_lines_list).to(have_len(2))
