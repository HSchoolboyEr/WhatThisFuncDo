import pytest
import pytest_asyncio
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))
from tools.raw_data_prepare.r2_metaData_extractor import WTF


wtf_test = WTF(os.path.join(os.path.dirname(__file__), 'small_ELF_for_test.o'))


@pytest.mark.asyncio
async def test_correct_parse_count_func():
    count_func = await wtf_test.get_functions_count()
    assert 2 == count_func


@pytest.mark.asyncio
async def test_correct_parse_ELF_format_to_ASM():
    dict_funcs_code = await wtf_test.get_functions_asm_code()
    assert 'sub rsp, 8\ncall ftello64\nxor edx, edx\nadd rsp, 8\nret\n' == dict_funcs_code['a61179b7167423c14048de849d671f45'][0]
