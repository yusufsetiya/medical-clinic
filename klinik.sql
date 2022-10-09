-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Waktu pembuatan: 09 Jan 2022 pada 13.46
-- Versi server: 10.4.21-MariaDB
-- Versi PHP: 8.0.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `klinik`
--

-- --------------------------------------------------------

--
-- Struktur dari tabel `berobat`
--

CREATE TABLE `berobat` (
  `id` int(11) NOT NULL,
  `pendaftaran_id` int(11) DEFAULT NULL,
  `waktu_daftar` datetime(6) DEFAULT NULL,
  `dokter_id` int(11) DEFAULT NULL,
  `keluhan` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Struktur dari tabel `dokter`
--

CREATE TABLE `dokter` (
  `id` int(11) NOT NULL,
  `akun_dokter` int(11) NOT NULL,
  `nama` varchar(255) DEFAULT NULL,
  `jadwal` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data untuk tabel `dokter`
--

INSERT INTO `dokter` (`id`, `akun_dokter`, `nama`, `jadwal`) VALUES
(11, 1, 'Dokter Tirtad', 'Senin - Rabud'),
(12, 1, 'Dokter Yusuf', 'Rabu - Jumat');

-- --------------------------------------------------------

--
-- Struktur dari tabel `obat`
--

CREATE TABLE `obat` (
  `id` int(11) NOT NULL,
  `namaobat` varchar(255) DEFAULT NULL,
  `jenisobat` varchar(255) DEFAULT NULL,
  `harga_beli` int(255) DEFAULT NULL,
  `harga_jual` int(255) DEFAULT NULL,
  `suplier_id` int(11) DEFAULT NULL,
  `kondisi` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Struktur dari tabel `pasien`
--

CREATE TABLE `pasien` (
  `id` bigint(20) NOT NULL,
  `pendaftaran_id` bigint(20) DEFAULT NULL,
  `dokter_id` varchar(255) DEFAULT NULL,
  `diagnosa` varchar(255) DEFAULT NULL,
  `resep` text DEFAULT NULL,
  `tanggal` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data untuk tabel `pasien`
--

INSERT INTO `pasien` (`id`, `pendaftaran_id`, `dokter_id`, `diagnosa`, `resep`, `tanggal`) VALUES
(19, 9, '11', 'www', 'www', '2022-01-04 00:00:00'),
(20, 10, '12', 'sas', 'asa', '2022-01-04 00:00:00'),
(21, 9, '12', 'sss', 'sss', '2022-01-04 00:00:00');

-- --------------------------------------------------------

--
-- Struktur dari tabel `pendaftaran`
--

CREATE TABLE `pendaftaran` (
  `id` bigint(20) NOT NULL,
  `nama` varchar(255) DEFAULT NULL,
  `tl` varchar(255) DEFAULT NULL,
  `tg_lahir` date DEFAULT NULL,
  `jk` varchar(255) DEFAULT NULL,
  `status` varchar(255) DEFAULT NULL,
  `profesi` varchar(255) DEFAULT NULL,
  `alamat` text DEFAULT NULL,
  `keterangan` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data untuk tabel `pendaftaran`
--

INSERT INTO `pendaftaran` (`id`, `nama`, `tl`, `tg_lahir`, `jk`, `status`, `profesi`, `alamat`, `keterangan`) VALUES
(9, 'Ardiyan', 'Malang', '2022-01-03', 'Laki-laki', 'Belum', 'Pekerja', 'Jl. Ambarawa', '0'),
(10, 'Ridho', 'Surabaya', '2022-01-05', 'Laki-laki', 'Sudah', 'Pegawai', 'Jl. Aguspara', '0');

-- --------------------------------------------------------

--
-- Struktur dari tabel `suplier`
--

CREATE TABLE `suplier` (
  `id` int(11) NOT NULL,
  `perusahaan` varchar(255) DEFAULT NULL,
  `kontak` varchar(255) DEFAULT NULL,
  `alamat` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Struktur dari tabel `user`
--

CREATE TABLE `user` (
  `id` int(11) NOT NULL,
  `dokter_id` int(11) NOT NULL,
  `username` varchar(255) DEFAULT NULL,
  `password` text DEFAULT NULL,
  `show_pwd` varchar(50) NOT NULL,
  `level` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data untuk tabel `user`
--

INSERT INTO `user` (`id`, `dokter_id`, `username`, `password`, `show_pwd`, `level`) VALUES
(22, 0, 'Ahmad Rizal123', '123123', '123123', 'Petugas'),
(26, 12, 'yusuf', '$2b$12$R0Rxss5xjicFfP8OBqYe7eEZNEQApMHesnudxy2Hq.HCDn04vKjUS', 'yusuf', 'Dokter'),
(28, 0, 'jojo', '$2b$12$mi8F2pnwwaIXyERiElYU4eCCuJLzPBXamqwUGQNJ468tTdJV62nTy', 'jojo', 'Admin'),
(29, 0, 'nana', '$2b$12$JAz9fGgdlqIlNAl0DDcvdOJkawgNnCobAKFjiKGcjesCgS69MZJjq', 'nana', 'Petugas'),
(30, 11, 'www', '$2b$12$/SAWgefDUuSmKGg9i1Ysa.fXZVchw5pf/.kVHLPGJcmMEu5LH5yua', 'www', 'Dokter');

--
-- Trigger `user`
--
DELIMITER $$
CREATE TRIGGER `update_dokter` AFTER DELETE ON `user` FOR EACH ROW UPDATE dokter SET akun_dokter='0'
WHERE id= OLD.dokter_id
$$
DELIMITER ;

--
-- Indexes for dumped tables
--

--
-- Indeks untuk tabel `berobat`
--
ALTER TABLE `berobat`
  ADD PRIMARY KEY (`id`);

--
-- Indeks untuk tabel `dokter`
--
ALTER TABLE `dokter`
  ADD PRIMARY KEY (`id`);

--
-- Indeks untuk tabel `obat`
--
ALTER TABLE `obat`
  ADD PRIMARY KEY (`id`);

--
-- Indeks untuk tabel `pasien`
--
ALTER TABLE `pasien`
  ADD PRIMARY KEY (`id`);

--
-- Indeks untuk tabel `pendaftaran`
--
ALTER TABLE `pendaftaran`
  ADD PRIMARY KEY (`id`);

--
-- Indeks untuk tabel `suplier`
--
ALTER TABLE `suplier`
  ADD PRIMARY KEY (`id`);

--
-- Indeks untuk tabel `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT untuk tabel yang dibuang
--

--
-- AUTO_INCREMENT untuk tabel `berobat`
--
ALTER TABLE `berobat`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=32;

--
-- AUTO_INCREMENT untuk tabel `dokter`
--
ALTER TABLE `dokter`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- AUTO_INCREMENT untuk tabel `pasien`
--
ALTER TABLE `pasien`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=25;

--
-- AUTO_INCREMENT untuk tabel `pendaftaran`
--
ALTER TABLE `pendaftaran`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT untuk tabel `user`
--
ALTER TABLE `user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=31;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
