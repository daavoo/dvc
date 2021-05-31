import pytest

from dvc.exceptions import InvalidArgumentError


def test_remove_added_file_as_target(tmp_dir, dvc):
    tmp_dir.gen("foo", "foo")

    dvc.add("foo")

    dvc.remove("foo")

    assert not (tmp_dir / ".gitignore").exists()
    assert not (tmp_dir / "foo.dvc").exists()
    assert (tmp_dir / "foo").exists()


def test_remove_added_file_as_target_with_dvc_suffix(tmp_dir, dvc):
    tmp_dir.gen("foo", "foo")

    dvc.add("foo")

    dvc.remove("foo.dvc")

    assert not (tmp_dir / ".gitignore").exists()
    assert not (tmp_dir / "foo.dvc").exists()
    assert (tmp_dir / "foo").exists()


def test_remove_added_dir_as_target(tmp_dir, dvc):
    tmp_dir.gen("foo/file1")
    tmp_dir.gen("foo/file2")

    dvc.add("foo")

    dvc.remove("foo")

    assert not (tmp_dir / ".gitignore").exists()
    assert not (tmp_dir / "foo.dvc").exists()
    assert (tmp_dir / "foo").exists()


def test_remove_added_file_in_subdir_as_target(tmp_dir, dvc):
    tmp_dir.gen("foo/file1")
    tmp_dir.gen("foo/file2")

    dvc.add("foo")

    with pytest.raises(InvalidArgumentError):
        dvc.remove("foo/file1")
