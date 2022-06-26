import os
from pprint import pprint

from expects import expect, equal, have_len
from mamba import description, it, before

from src.duplicated_lines_finder import DuplicatedLinesFinder
from src.duplicated_lines_repository import DuplicatedLinesRepository
from src.ast_generator import MyVisitor, parse_ast_of

with description('Repeated lines finder') as self:
    with description('in sample 1'):
        with before.each:
            path = os.path.dirname(os.path.realpath(__file__)) + '/sample_declarations_1.c'
            self.ast = parse_ast_of(path)

        with it('finds repeated lines in the sample 1'):
            repeated_lines_list = DuplicatedLinesFinder().find(self.ast)
            print("")
            pprint(repeated_lines_list)
            variable_names = [x['variable']['name'] for x in repeated_lines_list]
            expect(variable_names).to(equal(['key__repeated', 'counter__repeated']))
            expect(repeated_lines_list).to(have_len(2))
