import pytest

from aerographer.whiteboard import Whiteboard
from aerographer.exceptions import (
        WhiteboardCreateSectionError,
        WhiteboardGetSectionError,
        WhiteboardRemoveSectionError,
        WhiteboardWriteError,
        WhiteboardGetError,
        WhiteboardEraseError
    )


def test_create_valid_section() -> None:
    wb = Whiteboard()
    wb.new_section('test_section')
    assert 'test_section' in wb.board


def test_create_invalid_section() -> None:
    wb = Whiteboard()
    with pytest.raises(WhiteboardCreateSectionError):
        wb.new_section({})


def test_create_invalid_section_blank() -> None:
    wb = Whiteboard()
    with pytest.raises(WhiteboardCreateSectionError):
        wb.new_section('')


def test_overwrite_section() -> None:
    wb = Whiteboard()
    wb.new_section('test_section')
    wb.write(section='test_section', title='test_title', msg='test_message')
    wb.new_section('test_section')
    assert wb.board['test_section']['test_title'] == {'message':'test_message', 'signature': ''}


def test_get_valid_section() -> None:
    wb = Whiteboard()
    wb.new_section('test_section')
    assert wb.get_section('test_section') == {}


def test_get_invalid_section() -> None:
    wb = Whiteboard()
    with pytest.raises(WhiteboardGetSectionError):
        wb.get_section({})


def test_get_missing_section() -> None:
    wb = Whiteboard()
    with pytest.raises(WhiteboardGetSectionError):
        wb.get_section('test_section')


def test_remove_valid_section() -> None:
    wb = Whiteboard()
    wb.new_section('test_section')
    wb.remove_section('test_section')
    assert 'test_section' not in wb.board


def test_remove_invalid_section() -> None:
    wb = Whiteboard()
    with pytest.raises(WhiteboardRemoveSectionError):
        wb.remove_section({'foo':'bar'})


def test_remove_missing_section() -> None:
    wb = Whiteboard()
    with pytest.raises(WhiteboardRemoveSectionError):
        wb.remove_section('test_section')


def test_valid_write_without_signature() -> None:
    wb = Whiteboard()
    wb.new_section('test_section')
    wb.write(section='test_section', title='test_title', msg='test_message')
    assert wb.board['test_section']['test_title'] == {'message':'test_message', 'signature': ''}


def test_valid_write_with_signature() -> None:
    wb = Whiteboard()
    wb.new_section('test_section')
    wb.write(section='test_section', title='test_title', msg='test_message', signature='test_signature')
    assert wb.board['test_section']['test_title'] == {'message':'test_message', 'signature': 'test_signature'}


def test_invalid_write_with_blank_title() -> None:
    wb = Whiteboard()
    wb.new_section('test_section')
    with pytest.raises(WhiteboardWriteError):
        wb.write(section='test_section', title='', msg='test_message')


def test_valid_write_multiple_entries() -> None:
    wb = Whiteboard()
    wb.new_section('test_section')
    wb.write(section='test_section', title='test_title1', msg='test_message1')
    wb.write(section='test_section', title='test_title2', msg='test_message2')
    assert wb.board['test_section'] == {
        'test_title1': {'message':'test_message1', 'signature': ''},
        'test_title2': {'message':'test_message2', 'signature': ''}
    }


def test_valid_write_with_invalid_signature() -> None:
    wb = Whiteboard()
    wb.new_section('test_section')
    with pytest.raises(WhiteboardWriteError):
        wb.write(section='test_section', title='test_title', msg='test_message', signature={'foo':'bar'})


def test_valid_write_without_overwrite() -> None:
    wb = Whiteboard()
    wb.new_section('test_section')
    wb.write(section='test_section', title='test_title', msg='test_message')
    wb.write(section='test_section', title='test_title', msg='test_overwrite_message')
    assert wb.board['test_section']['test_title'] == {'message':'test_message', 'signature': ''}


def test_valid_write_with_overwrite() -> None:
    wb = Whiteboard()
    wb.new_section('test_section')
    wb.write(section='test_section', title='test_title', msg='test_message')
    wb.write(section='test_section', title='test_title', msg='test_overwrite_message', overwrite=True)
    assert wb.board['test_section']['test_title'] == {'message':'test_overwrite_message', 'signature': ''}


def test_invalid_title_write() -> None:
    wb = Whiteboard()
    wb.new_section('test_section')
    with pytest.raises(WhiteboardWriteError):
        wb.write(section='test_section', title={'foo':'bar'}, msg='test_message')


def test_valid_get_title_only() -> None:
    wb = Whiteboard()
    wb.new_section('test_section')
    wb.write(section='test_section', title='test_title1', msg='test_message1')
    wb.write(section='test_section', title='test_title2', msg='test_message2')
    assert wb.get(section='test_section', title='test_title1') == [{'message':'test_message1', 'signature': ''}]


def test_valid_get_signature_only() -> None:
    wb = Whiteboard()
    wb.new_section('test_section')
    wb.write(section='test_section', title='test_title1', msg='test_message1', signature='test_signature')
    wb.write(section='test_section', title='test_title2', msg='test_message2', signature='test_signature')
    assert wb.get(section='test_section', signature='test_signature') == [ {'message': 'test_message1', 'signature': 'test_signature'},
        {'message': 'test_message2', 'signature': 'test_signature'}    
    ]


def test_valid_get_title_and_signature() -> None:
    wb = Whiteboard()
    wb.new_section('test_section')
    wb.write(section='test_section', title='test_title1', msg='test_message1', signature='test_signature')
    wb.write(section='test_section', title='test_title2', msg='test_message2', signature='test_signature')
    assert wb.get(section='test_section', title='test_title1', signature='test_signature') == [{'message':'test_message1', 'signature': 'test_signature'}]


def test_valid_get_no_entry() -> None:
    wb = Whiteboard()
    wb.new_section('test_section')
    assert wb.get(section='test_section', title='test_title') == []


def test_invalid_title_get() -> None:
    wb = Whiteboard()
    wb.new_section('test_section')
    wb.write(section='test_section', title='test_title', msg='test_message')
    with pytest.raises(WhiteboardGetError):
        wb.get(section='test_section', title={'foo':'bar'})


def test_invalid_signature_get() -> None:
    wb = Whiteboard()
    wb.new_section('test_section')
    wb.write(section='test_section', title='test_title', msg='test_message')
    with pytest.raises(WhiteboardGetError):
        wb.get(section='test_section', signature={'foo':'bar'})


def test_valid_erase_title_only() -> None:
    wb = Whiteboard()
    wb.new_section('test_section')
    wb.write(section='test_section', title='test_title1', msg='test_message1')
    wb.write(section='test_section', title='test_title2', msg='test_message2')
    wb.erase(section='test_section', title='test_title1')
    assert wb.board['test_section'] == {
            'test_title2': {'message':'test_message2', 'signature': ''}
        }


def test_valid_erase_signature_only() -> None:
    wb = Whiteboard()
    wb.new_section('test_section')
    wb.write(section='test_section', title='test_title1', msg='test_message1', signature='test_signature1')
    wb.write(section='test_section', title='test_title2', msg='test_message2', signature='test_signature2')
    wb.erase(section='test_section', signature='test_signature1')
    assert wb.board['test_section'] == {
            'test_title2': {'message':'test_message2', 'signature': 'test_signature2'}
        }


def test_valid_erase_title_and_signature() -> None:
    wb = Whiteboard()
    wb.new_section('test_section')
    wb.write(section='test_section', title='test_title1', msg='test_message1', signature='test_signature1')
    wb.write(section='test_section', title='test_title2', msg='test_message2', signature='test_signature2')
    wb.erase(section='test_section', title='test_title1' ,signature='test_signature1')
    assert wb.board['test_section'] == {
            'test_title2': {'message':'test_message2', 'signature': 'test_signature2'}
        }


def test_invalid_erase_blank_title() -> None:
    wb = Whiteboard()
    wb.new_section('test_section')
    wb.write(section='test_section', title='test_title1', msg='test_message1')
    with pytest.raises(WhiteboardEraseError):
        wb.erase(section='test_section', title='test_title2')


def test_invalid_title_erase() -> None:
    wb = Whiteboard()
    wb.new_section('test_section')
    wb.write(section='test_section', title='test_title1', msg='test_message1')
    with pytest.raises(WhiteboardEraseError):
        wb.erase(section='test_section', title={'foo':'bar'})


def test_invalid_signature_erase() -> None:
    wb = Whiteboard()
    wb.new_section('test_section')
    wb.write(section='test_section', title='test_title1', msg='test_message1', signature='test_signature1')
    with pytest.raises(WhiteboardEraseError):
        wb.erase(section='test_section', signature={'foo':'bar'})


def test_valid_scribble() -> None:
    wb = Whiteboard()
    wb.scribble(title='test_title1', msg='test_message1')
    wb.scribble(title='test_title2', msg='test_message2')
    assert wb.board['scribbles'] == {
            'test_title1': 'test_message1',
            'test_title2': 'test_message2'
        }


def test_invalid_scribble_title_blank() -> None:
    wb = Whiteboard()
    with pytest.raises(WhiteboardWriteError):
        wb.scribble(title='', msg='test_message1')


def test_invalid_title_scribble() -> None:
    wb = Whiteboard()
    with pytest.raises(WhiteboardWriteError):
        wb.scribble(title={'foo':'bar'}, msg='test_message1')


def test_valid_get_scribble() -> None:
    wb = Whiteboard()
    wb.scribble(title='test_title', msg='test_message')
    assert wb.get_scribble(title='test_title') == 'test_message'


def test_valid_get_scribble_blank() -> None:
    wb = Whiteboard()
    assert wb.get_scribble(title='test_title') == None


def test_print(capfd) -> None:
    wb = Whiteboard()
    wb.new_section(section='test_section1')
    wb.write(section='test_section1', title='test_title1', msg='test_message1')
    wb.scribble(title='test_title1', msg='test_message1')
    wb.print()
    out, _ = capfd.readouterr()
    assert out == "\
============================================== scribbles ==============================================\n\
{'test_title1': 'test_message1'}\n\
\n\
============================================== test_section1 ==============================================\n\
{'test_title1': {'message': 'test_message1', 'signature': ''}}\n\n"