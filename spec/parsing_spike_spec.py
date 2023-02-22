import os
from pprint import pprint

import pycparser.c_generator
from expects import expect, equal, have_len
from mamba import description, it, before

from src.duplicated_lines_finder import DuplicatedLinesFinder, DuplicatedLinesRemover
from src.duplicated_lines_repository import DuplicatedLinesRepository
from src.ast_generator import MyVisitor, parse_ast_of


class CGenerator_With_Removing(pycparser.c_generator.CGenerator):

    def __init__(self, reduce_parentheses=False):
        super().__init__(reduce_parentheses)
        self.duplicated_lines = DuplicatedLinesRepository()

    # def visit_Decl(self, n, no_type=False):
    #     x1 = super().visit_Decl(n, no_type)
    #     try:
    #         v = n.children()[1][1].exprs
    #         if not self.duplicated_lines.register_assignment_and_maybe_remove_it(n, v):
    #             n.type = []
    #             return n
    #         else:
    #             return x1
    #     except IndexError:
    #         pass
    #     except AttributeError:
    #         pass
    #     return x1


with description('Repeated lines finder') as self:
    with description('in sample 1'):
        with before.each:
            path = os.path.dirname(os.path.realpath(__file__)) + '/sample_declarations_1.c'
            self.ast = parse_ast_of(path)

        with it('finds repeated lines in the sample 1'):
            repeated_lines_list = DuplicatedLinesFinder().find(self.ast)
            print("")
            pprint(repeated_lines_list)
            variable_names = [x.variable.name for x in repeated_lines_list]
            expect(variable_names).to(equal(['key__repeated', 'counter__repeated']))
            expect(repeated_lines_list).to(have_len(2))

        with it('removes lines in the sample 1'):
            # del self.ast.ext[-1]
            del self.ast.ext[-1].body.block_items[1]
            del self.ast.ext[-1].body.block_items[2]
            print(CGenerator_With_Removing().visit(self.ast))

            # pprint(new_ast)r
            # expect(new_ast).to(have_len(7))
            # print(pycparser.c_generator.CGenerator(reduce_parentheses=True).visit(self.ast))

